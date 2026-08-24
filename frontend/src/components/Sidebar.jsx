import { Link } from "react-router-dom";
import "./Sidebar.css";

export default function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="logo">
        <h2>Credit Risk</h2>
        <p>Admin Panel</p>
      </div>

      <nav className="menu">

        <Link to="/dashboard">Dashboard</Link>

        <Link to="/customers">Customers</Link>

        <Link to="/loans">Loans</Link>

        <Link to="/ai">AI Prediction</Link>

        <Link to="/blockchain">Blockchain</Link>

      </nav>

      <button
        className="logout-btn"
        onClick={() => {
          localStorage.removeItem("token");
          window.location.href = "/";
        }}
      >
        Logout
      </button>

    </aside>
  );
}