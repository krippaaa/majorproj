import React, { useEffect, useState } from "react";
import "./Dashboard.css";

import Layout from "../components/Layout";
import { getDashboardSummary } from "../services/dashboardService";
import { getCustomers } from "../services/customerService";

const Dashboard = () => {
  const [summary, setSummary] = useState({
    total_customers: 0,
    total_loans: 0,
    approved_loans: 0,
    pending_loans: 0,
    rejected_loans: 0,
    risk_summary: {
      High: 0,
      Medium: 0,
      Low: 0,
    },
  });

  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    loadDashboard();
    loadCustomers();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await getDashboardSummary();
      setSummary(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load dashboard");
    }
  };

  const loadCustomers = async () => {
    try {
      const data = await getCustomers();
      setCustomers(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load customers");
    }
  };

  return (
    <Layout>
      <div className="dashboard-container">
        <header className="dashboard-header">
          <h1>Credit Risk Assessment Dashboard</h1>
          <p className="subtitle">
            Blockchain & Machine Learning Based Loan Decision Support
          </p>
        </header>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Customers</h3>
            <h2>{summary.total_customers}</h2>
          </div>

          <div className="stat-card">
            <h3>Total Loans</h3>
            <h2>{summary.total_loans}</h2>
          </div>

          <div className="stat-card">
            <h3>Approved Loans</h3>
            <h2>{summary.approved_loans}</h2>
          </div>

          <div className="stat-card">
            <h3>Pending Loans</h3>
            <h2>{summary.pending_loans}</h2>
          </div>

          <div className="stat-card">
            <h3>Rejected Loans</h3>
            <h2>{summary.rejected_loans}</h2>
          </div>

          <div className="stat-card">
            <h3>Low Risk</h3>
            <h2>{summary.risk_summary.Low}</h2>
          </div>

          <div className="stat-card">
            <h3>Medium Risk</h3>
            <h2>{summary.risk_summary.Medium}</h2>
          </div>

          <div className="stat-card">
            <h3>High Risk</h3>
            <h2>{summary.risk_summary.High}</h2>
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
    </Layout>
  );
};

export default Dashboard;