#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from kenyan_foods import Foods, Food
from glucose_predictor import GlucosePredict
from gamification import Points, Badges


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

# Register API resources
api.add_resource(Foods, '/foods')
api.add_resource(Food, '/foods/<int:food_id>')
api.add_resource(GlucosePredict, '/predict')
api.add_resource(Points, '/users/<user_id>/points')
api.add_resource(Badges, '/users/<user_id>/badges')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

