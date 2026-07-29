import { Link } from "react-router-dom";
import {
  FaHome,
  FaUsers,
  FaMoneyCheckAlt,
  FaRobot,
  FaLink,
} from "react-icons/fa";

import "./Sidebar.css";

export default function Sidebar() {
  return (
    <div className="sidebar">

      <h2>AI Credit Risk</h2>

      <Link to="/">
        <FaHome /> Dashboard
      </Link>

      <Link to="/customers">
        <FaUsers /> Customers
      </Link>

      <Link to="/loans">
        <FaMoneyCheckAlt /> Loans
      </Link>

      <Link to="/ai">
        <FaRobot /> AI Prediction
      </Link>

      <Link to="/blockchain">
        <FaLink /> Blockchain
      </Link>

    </div>
  );
}