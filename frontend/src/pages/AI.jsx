import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { getPredictions } from "../services/predictionService";

export default function AI() {

  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    loadPredictions();
  }, []);

  const loadPredictions = async () => {
    try {
      const data = await getPredictions();
      setPredictions(data);
    } catch (err) {
      console.error(err);
      alert("Failed to load predictions.");
    }
  };

  const total = predictions.length;

  const low = predictions.filter(
    (p) => p.risk_category === "Low"
  ).length;

  const medium = predictions.filter(
    (p) => p.risk_category === "Medium"
  ).length;

  const high = predictions.filter(
    (p) => p.risk_category === "High"
  ).length;

  const avgConfidence =
    total === 0
      ? 0
      : (
          predictions.reduce(
            (sum, p) => sum + p.confidence,
            0
          ) / total
        ).toFixed(1);

  return (
    <Layout>

      <div className="dashboard-container">

        <h1>AI Credit Risk Prediction</h1>

        <p>
          Predictions generated using the Logistic Regression model.
        </p>

        <div className="stats-grid">

          <div className="stat-card">
            <h3>Total Predictions</h3>
            <h2>{total}</h2>
          </div>

          <div className="stat-card">
            <h3>Low Risk</h3>
            <h2>{low}</h2>
          </div>

          <div className="stat-card">
            <h3>Medium Risk</h3>
            <h2>{medium}</h2>
          </div>

          <div className="stat-card">
            <h3>High Risk</h3>
            <h2>{high}</h2>
          </div>

          <div className="stat-card">
            <h3>Average Confidence</h3>
            <h2>{avgConfidence}%</h2>
          </div>

        </div>

        <table className="loans-table">

          <thead>

            <tr>

              <th>Loan</th>

              <th>Customer</th>

              <th>Risk</th>

              <th>Confidence</th>

              <th>Model</th>

              <th>Date</th>

            </tr>

          </thead>

          <tbody>

            {predictions.map((prediction) => (

              <tr key={prediction.prediction_id}>

                <td>{prediction.loan_id}</td>

                <td>{prediction.customer_name}</td>

                <td>

                  {prediction.risk_category === "Low" && "🟢 Low"}

                  {prediction.risk_category === "Medium" && "🟡 Medium"}

                  {prediction.risk_category === "High" && "🔴 High"}

                </td>

                <td>{prediction.confidence}%</td>

                <td>{prediction.model_name}</td>

                <td>
                  {new Date(
                    prediction.predicted_at
                  ).toLocaleDateString()}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </Layout>
  );
}