import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Layout from "../components/Layout";
import api from "../api/api";

export default function CreateLoan() {
  const navigate = useNavigate();

  const [customers, setCustomers] = useState([]);

  const [form, setForm] = useState({
    customer_id: "",
    loan_amount: "",
    loan_purpose: "",
    loan_term: "",
    annual_income: "",
    employment_status: "",
    credit_score: "",
  });

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get("/customers/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setCustomers(response.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load customers.");
    }
  };

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const createLoan = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await api.post("/loans/", form, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      alert("Loan created successfully!");

      navigate("/loans");
    } catch (err) {
      console.error(err);
      alert("Failed to create loan.");
    }
  };

  return (
    <Layout>
      <div className="dashboard-container">

        <h1>Create Loan</h1>

        <form onSubmit={createLoan}>

          <select
            name="customer_id"
            value={form.customer_id}
            onChange={handleChange}
            required
          >
            <option value="">Select Customer</option>

            {customers.map((customer) => (
              <option
                key={customer.customer_id}
                value={customer.customer_id}
              >
                {customer.full_name}
              </option>
            ))}
          </select>

          <br /><br />

          <input
            type="number"
            name="loan_amount"
            placeholder="Loan Amount"
            value={form.loan_amount}
            onChange={handleChange}
            required
          />

          <br /><br />

          <input
            type="text"
            name="loan_purpose"
            placeholder="Loan Purpose"
            value={form.loan_purpose}
            onChange={handleChange}
          />

          <br /><br />

          <input
            type="number"
            name="loan_term"
            placeholder="Loan Term (Months)"
            value={form.loan_term}
            onChange={handleChange}
          />

          <br /><br />

          <input
            type="number"
            name="annual_income"
            placeholder="Annual Income"
            value={form.annual_income}
            onChange={handleChange}
          />

          <br /><br />

          <input
            type="text"
            name="employment_status"
            placeholder="Employment Status"
            value={form.employment_status}
            onChange={handleChange}
          />

          <br /><br />

          <input
            type="number"
            name="credit_score"
            placeholder="Credit Score"
            value={form.credit_score}
            onChange={handleChange}
          />

          <br /><br />

          <button type="submit">
            Create Loan
          </button>

        </form>

      </div>
    </Layout>
  );
}