import React, { useMemo, useState } from "react";

function SmartAlerts() {
  const [recent, setRecent] = useState("120, 135, 142");
  const [carbs, setCarbs] = useState("45");
  const [gi, setGi] = useState("55");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const parsedRecent = useMemo(() => {
    return recent
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
      .map((n) => Number(n));
  }, [recent]);

  function predict() {
    setLoading(true);
    setError(null);
    setResult(null);
    fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        recent_readings: parsedRecent,
        carbs: Number(carbs),
        gi: Number(gi),
      }),
    })
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => setResult(data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  function riskColor(risk) {
    if (risk === "low") return "#1e88e5";
    if (risk === "target") return "#2e7d32";
    if (risk === "elevated") return "#f9a825";
    if (risk === "high") return "#c62828";
    return "#555";
  }

  return (
    <div style={{ padding: 16 }}>
      <h2>Smart Alerts & Prediction</h2>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, maxWidth: 720 }}>
        <label>
          Recent Readings (mg/dL)
          <input
            style={{ display: "block", padding: 8, width: "100%" }}
            value={recent}
            onChange={(e) => setRecent(e.target.value)}
            placeholder="e.g. 120, 135, 142"
          />
        </label>
        <label>
          Food Carbs (g)
          <input
            style={{ display: "block", padding: 8, width: "100%" }}
            value={carbs}
            onChange={(e) => setCarbs(e.target.value)}
            type="number"
            min="0"
          />
        </label>
        <label>
          Food GI
          <input
            style={{ display: "block", padding: 8, width: "100%" }}
            value={gi}
            onChange={(e) => setGi(e.target.value)}
            type="number"
            min="0"
            max="100"
          />
        </label>
      </div>
      <div style={{ marginTop: 12 }}>
        <button onClick={predict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && (
        <div style={{ marginTop: 16, padding: 12, border: "1px solid #ddd" }}>
          <p>
            Predicted Glucose: <strong>{result.predicted_glucose} mg/dL</strong>
          </p>
          <p>
            Risk: <span style={{ color: riskColor(result.risk), fontWeight: 700 }}>{result.risk}</span>
          </p>
        </div>
      )}
    </div>
  );
}

export default SmartAlerts; 