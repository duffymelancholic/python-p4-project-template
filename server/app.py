#!/usr/bin/env python3

# Standard library imports
import json

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
from kenyan_foods import get_kenyan_food_database
from glucose_predictor import get_glucose_predictor
from gamification import get_gamification_system

# Add your model imports

# Initialize systems
food_db = get_kenyan_food_database()
predictor = get_glucose_predictor()
gamification = get_gamification_system()

# Views go here!

@app.route('/')
def index():
    return '<h1>HealthTracker API - Kenyan Localization Features</h1>'

# Kenyan Foods API
@app.route('/api/foods', methods=['GET'])
def get_foods():
    """Get all Kenyan foods or search by query"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    if query:
        foods = food_db.search_foods(query)
    elif category:
        foods = food_db.get_foods_by_category(category)
    else:
        foods = food_db.foods
    
    return jsonify([{
        'id': food.id,
        'name_english': food.name_english,
        'name_swahili': food.name_swahili,
        'category': food.category.value,
        'diabetes_friendly': food.diabetes_friendly,
        'nutritional_info': food.nutritional_info.__dict__,
        'description_english': food.description_english,
        'description_swahili': food.description_swahili
    } for food in foods])

@app.route('/api/foods/<food_id>', methods=['GET'])
def get_food_details(food_id):
    """Get detailed information about a specific food"""
    food = food_db.get_food_by_id(food_id)
    if not food:
        return jsonify({'error': 'Food not found'}), 404
    
    return jsonify({
        'id': food.id,
        'name_english': food.name_english,
        'name_swahili': food.name_swahili,
        'category': food.category.value,
        'diabetes_friendly': food.diabetes_friendly,
        'nutritional_info': food.nutritional_info.__dict__,
        'description_english': food.description_english,
        'description_swahili': food.description_swahili,
        'health_benefits': food.health_benefits,
        'preparation_tips': food.preparation_tips
    })

# Glucose Prediction API
@app.route('/api/predict-glucose', methods=['POST'])
def predict_glucose():
    """Predict glucose response to a meal"""
    data = request.get_json()
    
    # Mock user profile for demo
    from glucose_predictor import UserProfile
    user_profile = UserProfile(
        user_id="demo_user",
        age=data.get('age', 35),
        weight_kg=data.get('weight', 70),
        height_cm=data.get('height', 170)
    )
    
    prediction = predictor.predict_glucose_response(
        foods=data.get('foods', []),
        portions=data.get('portions', []),
        user_profile=user_profile,
        meal_context=data.get('context', {})
    )
    
    return jsonify(prediction)

# Gamification API
@app.route('/api/gamification/user/<user_id>', methods=['GET'])
def get_user_gamification(user_id):
    """Get user's gamification dashboard"""
    dashboard = gamification.get_user_dashboard(user_id)
    return jsonify(dashboard)

@app.route('/api/gamification/badges', methods=['GET'])
def get_badges():
    """Get all available badges"""
    badges = gamification.get_available_badges()
    return jsonify(badges)

@app.route('/api/gamification/challenges', methods=['GET'])
def get_challenges():
    """Get active challenges"""
    challenges = gamification.get_active_challenges()
    return jsonify(challenges)

@app.route('/api/gamification/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get community leaderboard"""
    limit = request.args.get('limit', 10, type=int)
    leaderboard = gamification.get_leaderboard(limit)
    return jsonify(leaderboard)

# Health Education API
@app.route('/api/education/modules', methods=['GET'])
def get_education_modules():
    """Get available education modules"""
    # Mock education modules data
    modules = [
        {
            'id': 'diabetes_basics',
            'title_english': 'Understanding Diabetes',
            'title_swahili': 'Kuelewa Kisukari',
            'category': 'basics',
            'difficulty': 'beginner',
            'duration': '15 min'
        },
        {
            'id': 'kenyan_foods_diabetes',
            'title_english': 'Kenyan Foods for Diabetes',
            'title_swahili': 'Vyakula vya Kenya kwa Kisukari',
            'category': 'nutrition',
            'difficulty': 'beginner',
            'duration': '20 min'
        }
    ]
    return jsonify(modules)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

