import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import CreditCardForm from "./CreditCardForm";

function App() {
  return (
    <div style={{
      background: 'linear-gradient(to right, #5D3FD3, #000000)',
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '20px'
    }}>
      <div className="container">
        <div className="row justify-content-center custom-form">
          <div className="col-lg-8">
            <div className="bg-white custom-form rounded border shadow p-4">
              <CreditCardForm />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
