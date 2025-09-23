import React, { useEffect, useState } from "react";

function Gamification() {
  const [userId, setUserId] = useState("1");
  const [points, setPoints] = useState(0);
  const [badges, setBadges] = useState([]);
  const [delta, setDelta] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function load() {
    setLoading(true);
    setError(null);
    Promise.all([
      fetch(`/users/${userId}/points`).then((r) => r.json()),
      fetch(`/users/${userId}/badges`).then((r) => r.json()),
    ])
      .then(([p, b]) => {
        setPoints(p.points || 0);
        setBadges(b.badges || []);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  function addPoints() {
    setLoading(true);
    setError(null);
    fetch(`/users/${userId}/points`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ delta }),
    })
      .then((r) => r.json())
      .then(() => load())
      .catch((e) => setError(e.message));
  }

  return (
    <div style={{ padding: 16 }}>
      <h2>Gamification</h2>
      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <label>
          User ID
          <input value={userId} onChange={(e) => setUserId(e.target.value)} style={{ marginLeft: 8, padding: 6 }} />
        </label>
        <button onClick={load} disabled={loading}>Refresh</button>
      </div>
      <div style={{ marginTop: 12 }}>
        <p>Points: <strong>{points}</strong></p>
        <p>Badges: {badges.length ? badges.join(", ") : "None"}</p>
      </div>
      <div style={{ marginTop: 12 }}>
        <label>
          Add Points
          <input type="number" value={delta} onChange={(e) => setDelta(Number(e.target.value))} style={{ marginLeft: 8, padding: 6 }} />
        </label>
        <button onClick={addPoints} disabled={loading} style={{ marginLeft: 8 }}>Add</button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Gamification; 