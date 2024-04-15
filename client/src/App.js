import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import CreditCardForm from "./CreditCardForm";

function App() {
  return (
    <div className="container mt-5">
      <h2 className="mb-4">Visage Payment Verification Prototype</h2>
      <CreditCardForm />
    </div>
  );
}

export default App;
