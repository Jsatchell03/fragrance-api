import React, { useState } from "react";
import logo from "./assets/scent-genie-logo.png";

import Select from "react-select";
import AIQueryForm from "./components/AIQueryForm";

const notes = [,];

export default function App() {
  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <img
        src={logo}
        alt="Logo"
        style={{
          width: "20rem",
          height: "auto",
          marginBottom: "0rem",
          marginTop: "5rem",
        }}
      />
      <AIQueryForm />
    </div>
  );
}
