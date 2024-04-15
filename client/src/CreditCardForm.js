import React, { useState } from "react";
import Cards from "react-credit-cards-2";
import "react-credit-cards-2/dist/es/styles-compiled.css";

const CreditCardForm = () => {
  const [state, setState] = useState({
    number: "",
    expiry: "",
    cvc: "",
    name: "",
    focus: "",
    verificationMessage: "",
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
    <div>
      <Cards
        number={state.number}
        expiry={state.expiry}
        cvc={state.cvc}
        name={state.name}
        focused={state.focus}
      />
      <div className="mt-3">
        <form>
          <div className="mb-3">
            <input
              type="number"
              name="number"
              className="form-control"
              placeholder="Card Number"
              value={state.number}
              onChange={handleInputChange}
              onFocus={handleInputFocus}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="text"
              name="name"
              className="form-control"
              placeholder="Name"
              onChange={handleInputChange}
              onFocus={handleInputFocus}
              required
            />
          </div>
          <div className="row">
            <div className="col-6 mb-3">
              <input
                type="number"
                name="expiry"
                className="form-control"
                placeholder="Valid Thru"
                pattern="\d\d/\d\d"
                value={state.expiry}
                onChange={handleInputChange}
                onFocus={handleInputFocus}
                required
              />
            </div>
            <div className="col-6 mb-3">
              <input
                type="number"
                name="cvc"
                className="form-control"
                placeholder="CVC"
                pattern="\d{3,4}"
                value={state.cvc}
                onChange={handleInputChange}
                onFocus={handleInputFocus}
                required
              />
            </div>
          </div>
          <div className="d-grid">
            <button className="btn btn-dark" onClick={handleVerify}>Confirm</button>
          </div>
        </form>
      </div>
      <p className="verification-message">{state.verificationMessage}</p>
    </div> 
  );
};

export default CreditCardForm;
