import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Electricians from "./Pages/Electricians";
import Header from "./Components/Header";
import Sites from "./Pages/Sites";

function App() {
  return (
    <>
  
      <Router>
       <Header/>

        <Routes>
          <Route path="/" element={<Electricians />} />
        </Routes>
        <Routes>
          <Route path="/sites" element={<Sites />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
