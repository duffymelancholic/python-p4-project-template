from flask import request
from flask_restful import Resource

# Simple in-memory Kenyan foods database for demo purposes
# In a real app, this could be backed by SQLAlchemy models
FOODS = [
    {"id": 1, "name": "Ugali", "carbs": 40, "gi": 56, "serving_grams": 200},
    {"id": 2, "name": "Sukuma Wiki", "carbs": 7, "gi": 15, "serving_grams": 100},
    {"id": 3, "name": "Githeri", "carbs": 30, "gi": 45, "serving_grams": 250},
    {"id": 4, "name": "Chapati", "carbs": 50, "gi": 62, "serving_grams": 120},
    {"id": 5, "name": "Nyama Choma", "carbs": 0, "gi": 0, "serving_grams": 150},
]


def find_food_by_id(food_id: int):
    for food in FOODS:
        if food["id"] == food_id:
            return food
    return None


def filter_foods_by_name(query: str):
    q = query.lower().strip()
    return [f for f in FOODS if q in f["name"].lower()]


class Foods(Resource):
    def get(self):
        # Optional search by name: /foods?search=uga
        search = request.args.get("search")
        if search:
            return filter_foods_by_name(search), 200
        return FOODS, 200


class Food(Resource):
    def get(self, food_id):
        food = find_food_by_id(int(food_id))
        if not food:
            return {"error": "Food not found"}, 404
        return food, 200 