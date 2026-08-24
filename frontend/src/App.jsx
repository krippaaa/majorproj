import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

import Customers from "./pages/Customers";
import Loans from "./pages/Loans";
import AI from "./pages/AI";
import Blockchain from "./pages/Blockchain";

import CreateLoan from "./pages/CreateLoan";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/customers" element={<Customers />} />

        <Route path="/loans" element={<Loans />} />

        <Route path="/create-loan" element={<CreateLoan />} />

        <Route path="/ai" element={<AI />} />

        <Route path="/blockchain" element={<Blockchain />} />

      </Routes>
    </BrowserRouter>
  );
}