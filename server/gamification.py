from flask import request
from flask_restful import Resource

# Minimal in-memory gamification store keyed by user_id
USER_POINTS = {}
USER_BADGES = {}

BADGE_THRESHOLDS = [
    (50, "Starter"),
    (150, "Consistent"),
    (300, "Champion"),
]


def compute_badges(points):
    badges = []
    for threshold, name in BADGE_THRESHOLDS:
        if points >= threshold:
            badges.append(name)
    return badges


class Points(Resource):
    def get(self, user_id):
        user_id = str(user_id)
        pts = USER_POINTS.get(user_id, 0)
        return {"user_id": user_id, "points": pts}, 200

    def post(self, user_id):
        user_id = str(user_id)
        payload = request.get_json(force=True, silent=True) or {}
        delta = int(payload.get("delta") or 0)
        USER_POINTS[user_id] = USER_POINTS.get(user_id, 0) + delta
        # refresh badges on point change
        USER_BADGES[user_id] = compute_badges(USER_POINTS[user_id])
        return {"user_id": user_id, "points": USER_POINTS[user_id]}, 200


class Badges(Resource):
    def get(self, user_id):
        user_id = str(user_id)
        pts = USER_POINTS.get(user_id, 0)
        badges = USER_BADGES.get(user_id) or compute_badges(pts)
        USER_BADGES[user_id] = badges
        return {"user_id": user_id, "badges": badges}, 200 