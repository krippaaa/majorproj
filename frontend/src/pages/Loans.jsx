import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import Layout from "../components/Layout";

import {
  getLoans,
  deleteLoan,
  updateLoanStatus,
} from "../services/loanService";

export default function Loans() {
  const [loans, setLoans] = useState([]);

  useEffect(() => {
    loadLoans();
  }, []);

  const loadLoans = async () => {
    try {
      const data = await getLoans();
      setLoans(data);
    } catch (err) {
      console.error(err);
      alert("Failed to load loans.");
    }
  };

  const approveLoan = async (id) => {
    try {
      await updateLoanStatus(id, "Approved");
      loadLoans();
    } catch (err) {
      console.error(err);
      alert("Failed to approve loan.");
    }
  };

  const rejectLoan = async (id) => {
    try {
      await updateLoanStatus(id, "Rejected");
      loadLoans();
    } catch (err) {
      console.error(err);
      alert("Failed to reject loan.");
    }
  };

  const removeLoan = async (id) => {
    if (!window.confirm("Delete this loan?")) return;

    try {
      await deleteLoan(id);
      loadLoans();
    } catch (err) {
      console.error(err);
      alert("Failed to delete loan.");
    }
  };

  return (
    <Layout>
      <div className="dashboard-container">

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <h1>Loan Applications</h1>

          <Link to="/create-loan">
            <button>Create New Loan</button>
          </Link>
        </div>

        <table className="loans-table">

          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Amount (NPR)</th>
              <th>Purpose</th>
              <th>Term</th>
              <th>AI Risk</th>
              <th>Confidence</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            {loans.map((loan) => (

              <tr key={loan.loan_id}>

                <td>{loan.loan_id}</td>

                <td>{loan.customer_name}</td>

                <td>
                  NPR {Number(loan.loan_amount).toLocaleString()}
                </td>

                <td>{loan.loan_purpose}</td>

                <td>{loan.loan_term} months</td>

                <td>
                  {loan.risk_category === "Low" && (
                    <span style={{ color: "green", fontWeight: "bold" }}>
                      🟢 Low
                    </span>
                  )}

                  {loan.risk_category === "Medium" && (
                    <span style={{ color: "orange", fontWeight: "bold" }}>
                      🟡 Medium
                    </span>
                  )}

                  {loan.risk_category === "High" && (
                    <span style={{ color: "red", fontWeight: "bold" }}>
                      🔴 High
                    </span>
                  )}

                  {loan.risk_category === "-" && "-"}
                </td>

                <td>{loan.confidence}%</td>

                <td>
                  {loan.status === "Approved" && (
                    <span style={{ color: "green", fontWeight: "bold" }}>
                      Approved
                    </span>
                  )}

                  {loan.status === "Pending" && (
                    <span style={{ color: "orange", fontWeight: "bold" }}>
                      Pending
                    </span>
                  )}

                  {loan.status === "Rejected" && (
                    <span style={{ color: "red", fontWeight: "bold" }}>
                      Rejected
                    </span>
                  )}
                </td>

                <td>

                  <button
                    onClick={() => approveLoan(loan.loan_id)}
                  >
                    Approve
                  </button>

                  {" "}

                  <button
                    onClick={() => rejectLoan(loan.loan_id)}
                  >
                    Reject
                  </button>

                  {" "}

                  <button
                    onClick={() => removeLoan(loan.loan_id)}
                  >
                    Delete
                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>
    </Layout>
  );
}