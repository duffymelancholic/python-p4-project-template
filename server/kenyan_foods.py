from flask import request
from flask_restful import Resource
from sqlalchemy import or_

from models import Food as FoodModel


class Foods(Resource):
    def get(self):
        search = request.args.get("search")
        query = FoodModel.query
        if search:
            like = f"%{search}%"
            query = query.filter(FoodModel.name.ilike(like))
        foods = [
            {
                "id": f.id,
                "name": f.name,
                "carbs": f.carbs,
                "gi": f.gi,
                "serving_grams": f.serving_grams,
            }
            for f in query.order_by(FoodModel.name.asc()).all()
        ]
        return foods, 200


class Food(Resource):
    def get(self, food_id):
        f = FoodModel.query.get(food_id)
        if not f:
            return {"error": "Food not found"}, 404
        return {
            "id": f.id,
            "name": f.name,
            "carbs": f.carbs,
            "gi": f.gi,
            "serving_grams": f.serving_grams,
        }, 200 