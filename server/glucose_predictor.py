from flask import request
from flask_restful import Resource

# Very naive heuristic predictor. In a real system, replace with ML model.
# Inputs: recent_readings: list of numbers (mg/dL), carbs: grams, gi: glycemic index
# Output: predicted_glucose in mg/dL and risk band.

def predict_glucose_next(recent_readings, carbs, gi):
    if not recent_readings:
        baseline = 110.0
    else:
        baseline = sum(recent_readings[-5:]) / min(len(recent_readings), 5)
    # crude estimate: impact proportional to carbs * gi factor
    gi_factor = (gi or 50) / 100.0
    food_impact = carbs * gi_factor * 0.8
    predicted = baseline + food_impact - 10  # assume some insulin or natural decay
    return max(60.0, min(predicted, 350.0))


def risk_band(glucose):
    if glucose < 70:
        return "low"
    if glucose <= 140:
        return "target"
    if glucose <= 200:
        return "elevated"
    return "high"


class GlucosePredict(Resource):
    def post(self):
        payload = request.get_json(force=True, silent=True) or {}
        recent = payload.get("recent_readings") or []
        carbs = float(payload.get("carbs") or 0)
        gi = float(payload.get("gi") or 50)
        try:
            recent = [float(x) for x in recent]
        except Exception:
            return {"error": "recent_readings must be numeric"}, 400
        predicted = predict_glucose_next(recent, carbs, gi)
        return {"predicted_glucose": round(predicted, 1), "risk": risk_band(predicted)}, 200 