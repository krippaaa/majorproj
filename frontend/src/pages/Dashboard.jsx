import React, { useEffect, useState } from "react";
import "./Dashboard.css";
import { getCustomers } from "../services/customerService";

const Dashboard = () => {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8001/customers/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    const data = await response.json();

    alert("Status: " + response.status);
    alert(JSON.stringify(data));

    setCustomers(data);
  } catch (error) {
    alert(error.message);
  }
};

  return (
    <div className="dashboard-container">

      <header className="dashboard-header">
        <h1>Blockchain and AI-Powered Credit Risk Assessment in Nepal Using Big Data </h1>
        <p className="subtitle">
          ML & Blockchain Based Loan Decision Support System
        </p>
      </header>

      <div className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Total Customers</h3>
            <p className="stat-number">{customers.length}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <h3>Loan Applications</h3>
            <p className="stat-number">0</p>
          </div>
        </div>

        <div className="stat-card approved">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Approved Loans</h3>
            <p className="stat-number">0</p>
          </div>
        </div>

        <div className="stat-card risk">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>High Risk</h3>
            <p className="stat-number">0</p>
          </div>
        </div>

      </div>

      <div className="recent-loans-section">
        <h2>Customers</h2>

        <table className="loans-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Citizenship</th>
              <th>Phone</th>
              <th>Email</th>
            </tr>
          </thead>

          <tbody>
            {customers.map((customer) => (
              <tr key={customer.customer_id}>
                <td>{customer.customer_id}</td>
                <td>{customer.full_name}</td>
                <td>{customer.citizenship_no}</td>
                <td>{customer.phone}</td>
                <td>{customer.email}</td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  );
};

export default Dashboard;