import React, { useEffect, useMemo, useState } from "react";

function FoodInsights() {
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    const url = query ? `/foods?search=${encodeURIComponent(query)}` : "/foods";
    setLoading(true);
    fetch(url, { signal: controller.signal })
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => {
        setFoods(data);
        setError(null);
      })
      .catch((e) => {
        if (e.name !== "AbortError") setError(e.message);
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [query]);

  const hasResults = useMemo(() => foods && foods.length > 0, [foods]);

  return (
    <div style={{ padding: 16 }}>
      <h2>Kenyan Food Insights</h2>
      <div style={{ marginBottom: 12 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search foods e.g. Ugali, Githeri"
          style={{ padding: 8, width: 320 }}
        />
      </div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!loading && !hasResults && <p>No foods found.</p>}
      {hasResults && (
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: 8 }}>Food</th>
              <th style={{ textAlign: "right", borderBottom: "1px solid #ddd", padding: 8 }}>Carbs (g)</th>
              <th style={{ textAlign: "right", borderBottom: "1px solid #ddd", padding: 8 }}>GI</th>
              <th style={{ textAlign: "right", borderBottom: "1px solid #ddd", padding: 8 }}>Serving (g)</th>
            </tr>
          </thead>
          <tbody>
            {foods.map((f) => (
              <tr key={f.id}>
                <td style={{ padding: 8 }}>{f.name}</td>
                <td style={{ padding: 8, textAlign: "right" }}>{f.carbs}</td>
                <td style={{ padding: 8, textAlign: "right" }}>{f.gi}</td>
                <td style={{ padding: 8, textAlign: "right" }}>{f.serving_grams}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default FoodInsights; 