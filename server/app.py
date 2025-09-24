#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

# Local imports
from config import app, db, api
from models import User, Reading, Medication, Meal, Doctor, Food, reading_meals
from schemas import UserSchema, ReadingSchema, MedicationSchema, MealSchema, DoctorSchema
from kenyan_foods import KENYAN_FOODS, get_food_recommendations, get_diabetes_friendly_foods, get_foods_to_limit, Foods, Food
from glucose_predictor import analyze_user_patterns, generate_predictive_alerts, get_meal_specific_predictions, get_food_impact_prediction, GlucosePredict
from gamification import BADGES, DAILY_CHALLENGES, get_user_progress, check_badges, get_daily_challenges_status, Points, Badges
from emergency_response import get_kenyan_emergency_system, EmergencyType, EmergencyPriority


# ---------------- Authentication ----------------
class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return {'error': 'Name, email, and password are required'}, 400
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'User with this email already exists'}, 400
        try:
            user = User(name=data['name'], email=data['email'])
            user.password_hash = data['password']
            if 'diabetes_type' in data:
                user.diabetes_type = data['diabetes_type']
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=user.id)
            return {
                'user': user.to_dict(),
                'access_token': access_token,
                'education': education_for(user.diabetes_type),
                'advice': advice_for(user)
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return {'error': 'Email and password are required'}, 400
        user = User.query.filter_by(email=data['email']).first()
        if user and user.authenticate(data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                'user': user.to_dict(),
                'access_token': access_token,
                'education': education_for(user.diabetes_type),
                'advice': advice_for(user)
            }, 200
        else:
            return {'error': 'Invalid email or password'}, 401

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            resp = user.to_dict()
            resp['education'] = education_for(user.diabetes_type)
            resp['advice'] = advice_for(user)
            return resp, 200
        else:
            return {'error': 'User not found'}, 404

@app.route('/')
def index():
    return '<h1>Diabetes Management API</h1>'

# Register API resources
api.add_resource(Foods, '/foods')
api.add_resource(Food, '/foods/<int:food_id>')
api.add_resource(GlucosePredict, '/predict')
api.add_resource(Points, '/users/<user_id>/points')
api.add_resource(Badges, '/users/<user_id>/badges')

# ---------------- Helpers (dates/times/validation) ----------------

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M').time()

def validate_glucose_value(value):
    try:
        v = float(value)
    except Exception:
        return False
    return 40 <= v <= 500

# ---------------- Diabetes education and advice ----------------
EDU = {
    'type1': [
        'Type 1 diabetes: autoimmune; requires insulin therapy.',
        'Monitor carbs and time insulin with meals.',
        'Carry fast-acting glucose to treat lows.'
    ],
    'type2': [
        'Type 2 diabetes: insulin resistance; lifestyle and meds help.',
        'Focus on weight management, low-GI carbs, regular activity.',
        'Monitor blood sugar trends and medication adherence.'
    ],
    'gestational': [
        'Gestational diabetes: occurs in pregnancy; close monitoring.',
        'Follow meal plan, stay active, and track sugars as advised.'
    ],
    'prediabetes': [
        'Prediabetes: elevated sugars; lifestyle changes are effective.',
        'Aim for 150+ minutes weekly activity and balanced meals.'
    ]
}

def education_for(diabetes_type):
    return EDU.get((diabetes_type or '').lower(), [])

def bmi_category_for(height_cm, weight_kg):
    try:
        if not height_cm or not weight_kg:
            return None
        h = float(height_cm) / 100.0
        bmi = float(weight_kg) / (h ** 2)
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    except Exception:
        return None

def advice_for(user):
    dtype = (user.diabetes_type or '').lower()
    bmi_cat = bmi_category_for(user.height_cm, user.weight_kg)
    base_nutrition = [
        'Prioritize whole foods: vegetables, lean proteins, healthy fats.',
        'Choose low-glycemic carbs and adequate fiber.',
        'Balance plates: half non-starchy veg, quarter protein, quarter carbs.'
    ]
    base_exercise = [
        'Aim for 150+ minutes/week of moderate activity (e.g., brisk walking).',
        'Add 2–3 days/week of resistance training if able.',
        'Light movement after meals (10–15 min) can help post-meal glucose.'
    ]
    base_med = [
        'Take medications exactly as prescribed.',
        'Discuss changes or side effects with your clinician.',
        'Never adjust insulin/meds without medical guidance.'
    ]

    if dtype == 'type1':
        base_nutrition += ['Count carbohydrates and match insulin appropriately.']
        base_exercise += ['Monitor glucose before/after exercise; carry fast-acting carbs.']
        base_med += ['Review basal/bolus strategy and correction factors with your care team.']
    elif dtype == 'type2':
        base_nutrition += ['Focus on weight management and portion control.']
        base_exercise += ['Build consistency; short daily walks are very effective.']
        base_med += ['Metformin adherence and timing can matter; ask about alternatives if GI side effects.']
    elif dtype == 'gestational':
        base_nutrition += ['Follow pregnancy meal plan and carb targets from your clinician.']
        base_exercise += ['Prefer low-impact activity as approved by your provider.']
        base_med += ['Frequent monitoring and close coordination with your obstetric team.']
    elif dtype == 'prediabetes':
        base_nutrition += ['Reduce sugary drinks and refined carbs; emphasize fiber.']
        base_exercise += ['Accumulate movement throughout the day; aim for daily consistency.']
        base_med += ['Lifestyle changes are first-line; discuss medication only if advised.']

    if bmi_cat == 'Underweight':
        base_nutrition += ['Ensure adequate calories and protein; seek a dietitian if losing weight unintentionally.']
    elif bmi_cat == 'Overweight':
        base_nutrition += ['Create a modest calorie deficit; consider smaller plates and mindful eating.']
        base_exercise += ['Start gently and build up duration; track steps to motivate progress.']
    elif bmi_cat == 'Obese':
        base_nutrition += ['Work with your clinician on a structured weight-loss plan; consider dietitian support.']
        base_exercise += ['Low-impact options (walking, cycling, swimming) reduce joint stress; progress gradually.']

    return {
        'nutrition': base_nutrition,
        'exercise': base_exercise,
        'medication': base_med,
        'bmi_category': bmi_cat,
    }

TIPS_NORMAL = [
    'Maintain balanced meals with non-starchy veggies, lean protein, and healthy fats.',
    'Stay hydrated and keep up light daily activity.',
    'Aim for consistent meal times and portion control.'
]
TIPS_HIGH = [
    'Take a 15–30 minute walk and hydrate with water.',
    'Reduce refined carbohydrates; choose low-GI, high-fiber foods.',
    'Include lean proteins and healthy fats to slow glucose spikes.',
    'Discuss supplements with your doctor (e.g., cinnamon, berberine).'
]

def evaluate_glucose(value, context):
    status = 'unknown'
    color = 'gray'
    suggestions = []
    if context == 'pre_meal':
        if 80 <= value <= 130:
            status, color, suggestions = 'normal', 'green', TIPS_NORMAL
        elif value > 130:
            status, color, suggestions = 'high', 'red', TIPS_HIGH
        else:
            status, color, suggestions = 'low', 'yellow', ['Consider a small balanced snack and consult your clinician if frequent.']
    else:
        if value < 180:
            status, color, suggestions = 'normal', 'green', TIPS_NORMAL
        elif value >= 180:
            status, color, suggestions = 'high', 'red', TIPS_HIGH
    return {'status': status, 'color': color, 'suggestions': suggestions}

user_schema = UserSchema()
reading_schema = ReadingSchema()
readings_schema = ReadingSchema(many=True)
medication_schema = MedicationSchema()
medications_schema = MedicationSchema(many=True)
meal_schema = MealSchema()
meals_schema = MealSchema(many=True)
doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)


# ---------------- Readings CRUD ----------------
class Readings(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        items = Reading.query.filter_by(user_id=user_id).order_by(Reading.date, Reading.time).all()
        return readings_schema.dump(items), 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        required = ['value', 'date', 'time']
        if not all(k in data for k in required):
            return {'error': 'value, date (YYYY-MM-DD), and time (HH:MM) are required'}, 400
        if not validate_glucose_value(data['value']):
            return {'error': 'value must be a number between 40 and 500'}, 400
        context = data.get('context')
        if context and context not in ['pre_meal', 'post_meal']:
            return {'error': "context must be 'pre_meal' or 'post_meal'"}, 400
        try:
            reading = Reading(
                value=float(data['value']),
                date=parse_date(data['date']),
                time=parse_time(data['time']),
                notes=data.get('notes'),
                context=context,
                user_id=user_id,
            )
            db.session.add(reading)
            db.session.commit()
            payload = reading_schema.dump(reading)
            if context:
                payload['evaluation'] = evaluate_glucose(reading.value, context)
            return payload, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class ReadingById(Resource):
    @jwt_required()
    def get(self, id):
        user_id = get_jwt_identity()
        reading = Reading.query.filter_by(id=id, user_id=user_id).first()
        if not reading:
            return {'error': 'Reading not found'}, 404
        payload = reading_schema.dump(reading)
        if reading.context:
            payload['evaluation'] = evaluate_glucose(reading.value, reading.context)
        return payload, 200

    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()
        reading = Reading.query.filter_by(id=id, user_id=user_id).first()
        if not reading:
            return {'error': 'Reading not found'}, 404
        data = request.get_json()
        if 'value' in data:
            if not validate_glucose_value(data['value']):
                return {'error': 'value must be a number between 40 and 500'}, 400
            reading.value = float(data['value'])
        if 'date' in data:
            reading.date = parse_date(data['date'])
        if 'time' in data:
            reading.time = parse_time(data['time'])
        if 'notes' in data:
            reading.notes = data['notes']
        if 'context' in data:
            if data['context'] not in ['pre_meal', 'post_meal', None]:
                return {'error': "context must be 'pre_meal' or 'post_meal'"}, 400
            reading.context = data['context']
        try:
            db.session.commit()
            payload = reading_schema.dump(reading)
            if reading.context:
                payload['evaluation'] = evaluate_glucose(reading.value, reading.context)
            return payload, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        reading = Reading.query.filter_by(id=id, user_id=user_id).first()
        if not reading:
            return {'error': 'Reading not found'}, 404
        try:
            db.session.delete(reading)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

# Register resources
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Readings, '/readings')
api.add_resource(ReadingById, '/readings/<int:id>')

# ---------------- Profile + BMI ----------------
class UserProfile(Resource):
    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        data = request.get_json()
        if 'name' in data and data['name']:
            user.name = data['name']
        if 'diabetes_type' in data:
            user.diabetes_type = data['diabetes_type'] or None
        if 'doctor_id' in data:
            user.doctor_id = data['doctor_id']
        if 'height_cm' in data:
            try:
                user.height_cm = float(data['height_cm']) if data['height_cm'] is not None else None
            except Exception:
                return {'error': 'height_cm must be a number'}, 400
        if 'weight_kg' in data:
            try:
                user.weight_kg = float(data['weight_kg']) if data['weight_kg'] is not None else None
            except Exception:
                return {'error': 'weight_kg must be a number'}, 400
        try:
            db.session.commit()
            resp = user_schema.dump(user)
            resp['education'] = education_for(user.diabetes_type)
            resp['advice'] = advice_for(user)
            return resp, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class UserBMI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        if not user.height_cm or not user.weight_kg:
            return {'error': 'height_cm and weight_kg must be set on profile'}, 400
        height_m = user.height_cm / 100.0
        bmi = user.weight_kg / (height_m ** 2)
        if bmi < 18.5:
            category = 'Underweight'
        elif bmi < 25:
            category = 'Normal'
        elif bmi < 30:
            category = 'Overweight'
        else:
            category = 'Obese'
        return {'bmi': round(bmi, 1), 'category': category}, 200

api.add_resource(UserProfile, '/me')
api.add_resource(UserBMI, '/me/bmi')

# ---------------- Medications (create/read + update status) ----------------
class Medications(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        meds = Medication.query.filter_by(user_id=user_id).order_by(Medication.time).all()
        return medications_schema.dump(meds), 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        required = ['name', 'dose', 'time']
        if not all(k in data and data[k] for k in required):
            return {'error': 'name, dose, and time (HH:MM) are required'}, 400
        try:
            med = Medication(
                name=data['name'].strip(),
                dose=data['dose'].strip(),
                time=parse_time(data['time']),
                status=(data.get('status') or 'pending'),
                user_id=user_id,
            )
            db.session.add(med)
            db.session.commit()
            return medication_schema.dump(med), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class MedicationById(Resource):
    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()
        med = Medication.query.filter_by(id=id, user_id=user_id).first()
        if not med:
            return {'error': 'Medication not found'}, 404
        data = request.get_json()
        if 'status' in data:
            if data['status'] not in ['pending', 'taken', 'missed']:
                return {'error': "status must be 'pending', 'taken', or 'missed'"}, 400
            med.status = data['status']
        if 'time' in data:
            med.time = parse_time(data['time'])
        if 'name' in data and data['name']:
            med.name = data['name'].strip()
        if 'dose' in data and data['dose']:
            med.dose = data['dose'].strip()
        try:
            db.session.commit()
            return medication_schema.dump(med), 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

api.add_resource(Medications, '/medications')
api.add_resource(MedicationById, '/medications/<int:id>')

# ---------------- Meals (create/read) ----------------
class Meals(Resource):
    @jwt_required()
    def get(self):
        meals = Meal.query.order_by(Meal.created_at.desc()).all()
        return meals_schema.dump(meals), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data.get('name'):
            return {'error': 'name is required'}, 400
        meal = Meal(
            name=data['name'].strip(),
            meal_type=data.get('meal_type'),
            description=data.get('description'),
        )
        try:
            db.session.add(meal)
            db.session.commit()
            return meal_schema.dump(meal), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

api.add_resource(Meals, '/meals')

# ---------------- Link/Unlink Meals to Readings with carbs_amount ----------------
class ReadingMeals(Resource):
    @jwt_required()
    def post(self, reading_id):
        user_id = get_jwt_identity()
        reading = Reading.query.filter_by(id=reading_id, user_id=user_id).first()
        if not reading:
            return {'error': 'Reading not found'}, 404
        data = request.get_json()
        if not data or not data.get('meal_id'):
            return {'error': 'meal_id is required'}, 400
        meal = Meal.query.get(data['meal_id'])
        if not meal:
            return {'error': 'Meal not found'}, 404
        carbs_amount = data.get('carbs_amount')
        try:
            ins = reading_meals.insert().values(
                reading_id=reading.id,
                meal_id=meal.id,
                carbs_amount=carbs_amount,
            )
            db.session.execute(ins)
            db.session.commit()
            return {'message': 'linked', 'reading_id': reading.id, 'meal_id': meal.id, 'carbs_amount': carbs_amount}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, reading_id):
        user_id = get_jwt_identity()
        reading = Reading.query.filter_by(id=reading_id, user_id=user_id).first()
        if not reading:
            return {'error': 'Reading not found'}, 404
        meal_id = request.args.get('meal_id', type=int)
        if not meal_id:
            return {'error': 'meal_id query param is required'}, 400
        try:
            delete_stmt = reading_meals.delete().where(
                (reading_meals.c.reading_id == reading.id) & (reading_meals.c.meal_id == meal_id)
            )
            db.session.execute(delete_stmt)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

api.add_resource(ReadingMeals, '/readings/<int:reading_id>/meals')

# ---------------- Doctors (create/list and list patients) ----------------
class Doctors(Resource):
    def get(self):
        items = Doctor.query.order_by(Doctor.id.desc()).all()
        return doctors_schema.dump(items), 200

    def post(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('email'):
            return {'error': 'name and email are required'}, 400
        if Doctor.query.filter_by(email=data['email']).first():
            return {'error': 'Doctor with this email already exists'}, 400
        try:
            doc = Doctor(name=data['name'].strip(), email=data['email'].strip())
            db.session.add(doc)
            db.session.commit()
            return doctor_schema.dump(doc), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400

class DoctorPatients(Resource):
    def get(self, doctor_id):
        doc = Doctor.query.get(doctor_id)
        if not doc:
            return {'error': 'Doctor not found'}, 404
        patients = [u.to_dict() for u in doc.patients]
        return {'doctor': doctor_schema.dump(doc), 'patients': patients}, 200

api.add_resource(Doctors, '/doctors')
api.add_resource(DoctorPatients, '/doctors/<int:doctor_id>/patients')

# ---------------- Kenyan Food Database ----------------
class KenyanFoods(Resource):
    def get(self):
        return {'foods': KENYAN_FOODS}, 200

class FoodRecommendations(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        language = request.args.get('lang', 'en')
        diabetes_type = user.diabetes_type or 'type2'
        recommendations = get_food_recommendations(diabetes_type, language)
        friendly_foods = get_diabetes_friendly_foods()
        foods_to_limit = get_foods_to_limit()
        return {
            'recommendations': recommendations,
            'diabetes_friendly': list(friendly_foods.keys()),
            'foods_to_limit': list(foods_to_limit.keys()),
            'diabetes_type': diabetes_type
        }, 200

api.add_resource(KenyanFoods, '/kenyan-foods')
api.add_resource(FoodRecommendations, '/food-recommendations')

# ---------------- Predictive Glucose Alerts ----------------
class GlucoseAlerts(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        language = request.args.get('lang', 'en')
        from datetime import date, timedelta
        cutoff_date = date.today() - timedelta(days=30)
        recent_readings = Reading.query.filter(
            Reading.user_id == user_id,
            Reading.date >= cutoff_date
        ).order_by(Reading.date.desc(), Reading.time.desc()).all()
        if len(recent_readings) < 3:
            return {
                'alerts': [],
                'message': 'Need more readings to generate predictions' if language == 'en' else 'Inahitaji vipimo zaidi ili kutoa utabiri'
            }, 200
        patterns = analyze_user_patterns(recent_readings)
        alerts = generate_predictive_alerts(user, patterns, language)
        return {
            'alerts': alerts,
            'patterns_summary': {
                'total_readings': len(recent_readings),
                'high_readings': patterns.get('high_readings_count', 0),
                'low_readings': patterns.get('low_readings_count', 0),
                'recent_trend': patterns.get('recent_trend', 'stable'),
                'avg_pre_meal': patterns.get('avg_pre_meal'),
                'avg_post_meal': patterns.get('avg_post_meal')
            }
        }, 200

class MealPrediction(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data or 'context' not in data:
            return {'error': 'context (pre_meal/post_meal) is required'}, 400
        language = data.get('language', 'en')
        meal_context = data['context']
        from datetime import date, timedelta
        cutoff_date = date.today() - timedelta(days=14)
        recent_readings = Reading.query.filter(
            Reading.user_id == user_id,
            Reading.date >= cutoff_date
        ).order_by(Reading.date.desc()).all()
        predictions = get_meal_specific_predictions(recent_readings, meal_context, language)
        return {'predictions': predictions}, 200

class FoodImpactPredictor(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data or 'food_name' not in data:
            return {'error': 'food_name is required'}, 400
        language = data.get('language', 'en')
        food_name = data['food_name']
        from datetime import date, timedelta
        cutoff_date = date.today() - timedelta(days=30)
        recent_readings = Reading.query.filter(
            Reading.user_id == user_id,
            Reading.date >= cutoff_date
        ).order_by(Reading.date.desc()).all()
        patterns = analyze_user_patterns(recent_readings) if recent_readings else None
        prediction = get_food_impact_prediction(food_name, patterns, language)
        if not prediction:
            return {'error': 'Food not found in database'}, 404
        return {'prediction': prediction}, 200

api.add_resource(GlucoseAlerts, '/glucose-alerts')
api.add_resource(MealPrediction, '/meal-prediction')
api.add_resource(FoodImpactPredictor, '/food-impact')

# ---------------- Emergency Response System ----------------
class EmergencyProtocols(Resource):
    def get(self):
        """Get all emergency protocols"""
        emergency_system = get_kenyan_emergency_system()
        protocols = {}
        for emergency_type, protocol in emergency_system.emergency_protocols.items():
            protocols[emergency_type.value] = {
                'emergency_type': emergency_type.value,
                'priority': protocol.priority.value,
                'immediate_actions': {
                    'english': protocol.immediate_actions_english,
                    'swahili': protocol.immediate_actions_swahili
                },
                'warning_signs': {
                    'english': protocol.warning_signs_english,
                    'swahili': protocol.warning_signs_swahili
                },
                'when_to_call_999': protocol.when_to_call_999,
                'when_to_call_doctor': protocol.when_to_call_doctor,
                'prevention_tips': {
                    'english': protocol.prevention_tips_english,
                    'swahili': protocol.prevention_tips_swahili
                }
            }
        return {'protocols': protocols}, 200

class EmergencyResponse(Resource):
    @jwt_required()
    def post(self):
        """Trigger emergency response"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return {'error': 'Request data required'}, 400
            
        # Get emergency parameters
        emergency_type_str = data.get('emergency_type', 'general_emergency')
        severity_level = data.get('severity_level', 5)
        user_location = data.get('location')  # [lat, lon]
        
        try:
            emergency_type = EmergencyType(emergency_type_str)
        except ValueError:
            emergency_type = EmergencyType.GENERAL_EMERGENCY
            
        # Convert location to tuple if provided
        location_tuple = None
        if user_location and len(user_location) == 2:
            location_tuple = (float(user_location[0]), float(user_location[1]))
            
        emergency_system = get_kenyan_emergency_system()
        
        # Trigger emergency response
        response = emergency_system.trigger_emergency_response(
            user_id=str(user_id),
            emergency_type=emergency_type,
            severity_level=severity_level,
            user_location=location_tuple
        )
        
        # Convert response to serializable format
        return {
            'emergency_id': response.emergency_id,
            'emergency_type': response.emergency_type.value,
            'severity_level': response.severity_level,
            'timestamp': response.timestamp.isoformat(),
            'nearest_hospitals': [{
                'name': h.name,
                'location': h.location,
                'phone': h.phone_number,
                'emergency_phone': h.emergency_phone,
                'has_diabetes_specialist': h.has_diabetes_specialist,
                'coordinates': h.coordinates
            } for h in response.nearest_hospitals],
            'protocol': {
                'priority': response.protocol_followed.priority.value,
                'immediate_actions_english': response.protocol_followed.immediate_actions_english,
                'immediate_actions_swahili': response.protocol_followed.immediate_actions_swahili,
                'when_to_call_999': response.protocol_followed.when_to_call_999
            },
            'emergency_numbers': emergency_system.get_emergency_numbers()
        }, 201

class EmergencyAssessment(Resource):
    @jwt_required()
    def post(self):
        """Assess emergency severity based on symptoms"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return {'error': 'Symptoms data required'}, 400
            
        emergency_system = get_kenyan_emergency_system()
        emergency_type, severity = emergency_system.assess_emergency_severity(data)
        
        protocol = emergency_system.get_emergency_protocol(emergency_type)
        
        return {
            'emergency_type': emergency_type.value,
            'severity_level': severity,
            'recommended_action': 'Call 999 immediately' if severity >= 8 else 'Seek medical attention',
            'protocol': {
                'priority': protocol.priority.value if protocol else 'medium',
                'immediate_actions_english': protocol.immediate_actions_english if protocol else [],
                'immediate_actions_swahili': protocol.immediate_actions_swahili if protocol else []
            }
        }, 200

class EmergencyNumbers(Resource):
    def get(self):
        """Get Kenyan emergency contact numbers"""
        emergency_system = get_kenyan_emergency_system()
        return {
            'emergency_numbers': emergency_system.get_emergency_numbers(),
            'country': 'Kenya',
            'instructions': {
                'english': 'Call 999 for any life-threatening emergency',
                'swahili': 'Piga 999 kwa dharura yoyote ya hatari ya maisha'
            }
        }, 200

class NearestHospitals(Resource):
    def post(self):
        """Find nearest hospitals to given location"""
        data = request.get_json()
        
        if not data or 'location' not in data:
            return {'error': 'Location [latitude, longitude] required'}, 400
            
        location = data['location']
        if not isinstance(location, list) or len(location) != 2:
            return {'error': 'Location must be [latitude, longitude] array'}, 400
            
        max_distance = data.get('max_distance_km', 50)
        
        emergency_system = get_kenyan_emergency_system()
        hospitals_with_distance = emergency_system.find_nearest_hospitals(
            float(location[0]), float(location[1]), max_distance
        )
        
        hospitals = []
        for hospital, distance in hospitals_with_distance:
            hospitals.append({
                'name': hospital.name,
                'location': hospital.location,
                'county': hospital.county,
                'distance_km': round(distance, 2),
                'phone': hospital.phone_number,
                'emergency_phone': hospital.emergency_phone,
                'has_diabetes_specialist': hospital.has_diabetes_specialist,
                'has_icu': hospital.has_icu,
                'has_emergency_room': hospital.has_emergency_room,
                'nhif_accredited': hospital.nhif_accredited,
                'estimated_response_time_minutes': hospital.estimated_response_time_minutes,
                'languages_supported': hospital.languages_supported,
                'coordinates': hospital.coordinates
            })
            
        return {
            'nearest_hospitals': hospitals,
            'search_location': location,
            'max_distance_km': max_distance
        }, 200

# Register emergency response endpoints
api.add_resource(EmergencyProtocols, '/emergency/protocols')
api.add_resource(EmergencyResponse, '/emergency/trigger')
api.add_resource(EmergencyAssessment, '/emergency/assess')
api.add_resource(EmergencyNumbers, '/emergency/numbers')
api.add_resource(NearestHospitals, '/emergency/hospitals')
