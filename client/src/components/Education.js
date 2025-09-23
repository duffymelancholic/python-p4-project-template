import React from "react";
import { useI18n } from "../contexts/LanguageContext";

function Education() {
  const { t } = useI18n();
  return (
    <div style={{ padding: 16 }}>
      <h2>{t("education_title")}</h2>
      <ul>
        <li>Understanding Type 2 Diabetes</li>
        <li>Glycemic Index in Kenyan Foods</li>
        <li>Monitoring Blood Glucose</li>
        <li>Physical Activity Tips</li>
        <li>Hypoglycemia and Hyperglycemia Safety</li>
      </ul>
      <p>More interactive modules can be added here.</p>
    </div>
  );
}

export default Education; 