import React, { useState } from "react";
import Cards from "react-credit-cards-2";
import "react-credit-cards-2/dist/es/styles-compiled.css";
import "./CreditCardForm.css";

const CreditCardForm = () => {
  const [state, setState] = useState({
    number: "",
    expiry: "",
    cvc: "",
    name: "",
    focus: "",
    verificationMessage: "",
    verificationStatus: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setState((prev) => ({ ...prev, [name]: value }));
  };

  const handleInputFocus = (e) => {
    setState((prev) => ({ ...prev, focus: e.target.name }));
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/receive_card_details', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ card_number: state.number, cvv: state.cvc })
      });
      const data = await response.json();
      setState(prevState => ({ 
        ...prevState, 
        verificationMessage: data.message,
        verificationStatus: data.success ? 'success' : 'error',
        number: "", 
        cvc: "",   
        expiry: "", 
        name: "",  
      }));
    } catch (error) {
      console.error('Error verifying:', error);
    }
  };

  return (
    <div className="position-relative custom-form">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="text-black mt-3 ms-3 custom-heading">Verify Card Details</h5>
        <button type="button" className="btn-close me-3" aria-label="Close"></button>
      </div>
      <hr className="mt-2 mb-4 mx-3" /> 
      <div className="mt-3"> 
        <Cards
          number={state.number}
          expiry={state.expiry}
          cvc={state.cvc}
          name={state.name}
          focused={state.focus}
        />
      </div>
      <div className="mt-3">
        <form>
          {/* Input fields */}
          <div className="d-flex flex-column flex-md-row">
            <div className="col-md-6 mb-3">
              <label htmlFor="number" className="form-label">Card Number</label>
              <input
                type="number"
                id="number"
                name="number"
                className="form-control"
                placeholder="Enter card number"
                value={state.number}
                onChange={handleInputChange}
                onFocus={handleInputFocus}
                required
              />
            </div>
            <div className="col-md-6 mb-3">
              <label htmlFor="cvc" className="form-label">CVC</label>
              <input
                type="number"
                id="cvc"
                name="cvc"
                className="form-control"
                placeholder="Enter CVC"
                pattern="\d{3,4}"
                value={state.cvc}
                onChange={handleInputChange}
                onFocus={handleInputFocus}
                required
              />
            </div>
          </div>
          <div className="mb-3">
            <label htmlFor="name" className="form-label">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              className="form-control"
              placeholder="Enter name"
              value={state.name}
              onChange={handleInputChange}
              onFocus={handleInputFocus}
              required
            />
          </div>
          <div className="row">
            <div className="col-md-6 mb-3">
              <label htmlFor="expiry" className="form-label">Expiration Date</label>
              <input
                type="text"
                id="expiry"
                name="expiry"
                className="form-control"
                placeholder="MM/YY"
                pattern="\d\d/\d\d"
                value={state.expiry}
                onChange={handleInputChange}
                onFocus={handleInputFocus}
                required
              />
            </div>
          </div>
          <div className="d-grid">
            <button className="btn btn-primary" onClick={handleVerify}>Confirm</button>
          </div>
        </form>
      </div>
      {/* Verification message */}
      <div className={`verification-message mt-3 p-3 text-white ${state.verificationStatus === 'success' ? 'bg-success' : state.verificationStatus === 'error' ? 'bg-danger' : ''}`}>
        {state.verificationMessage}
      </div>
    </div>
  );
};

export default CreditCardForm;
