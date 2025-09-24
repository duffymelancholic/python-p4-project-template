import React, { useEffect, useState } from "react";
import { useI18n } from "../contexts/LanguageContext";

function Gamification() {
  const { t } = useI18n();
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
      <h2>{t("gamification_title")}</h2>
      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <label>
          {t("user_id")}
          <input value={userId} onChange={(e) => setUserId(e.target.value)} style={{ marginLeft: 8, padding: 6 }} />
        </label>
        <button onClick={load} disabled={loading}>{t("refresh")}</button>
      </div>
      <div style={{ marginTop: 12 }}>
        <p>{t("points")}: <strong>{points}</strong></p>
        <p>{t("badges")}: {badges.length ? badges.join(", ") : "None"}</p>
      </div>
      <div style={{ marginTop: 12 }}>
        <label>
          {t("add_points")}
          <input type="number" value={delta} onChange={(e) => setDelta(Number(e.target.value))} style={{ marginLeft: 8, padding: 6 }} />
        </label>
        <button onClick={addPoints} disabled={loading} style={{ marginLeft: 8 }}>{t("add")}</button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Gamification; 