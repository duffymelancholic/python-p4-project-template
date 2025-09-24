from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, date

from config import db

# Kenyan Health App Database Models

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Personal Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(15))
    
    # Location (Kenyan-specific)
    county = db.Column(db.String(50))
    sub_county = db.Column(db.String(50))
    location = db.Column(db.String(100))
    
    # Health Profile
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    diabetes_type = db.Column(SQLEnum('type_1', 'type_2', 'gestational', 'prediabetes', name='diabetes_types'))
    diagnosis_date = db.Column(db.Date)
    
    # Preferences
    preferred_language = db.Column(db.String(10), default='english')
    nhif_number = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(15))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    glucose_readings = db.relationship('GlucoseReading', backref='user', lazy=True, cascade='all, delete-orphan')
    food_logs = db.relationship('FoodLog', backref='user', lazy=True, cascade='all, delete-orphan')
    exercise_logs = db.relationship('ExerciseLog', backref='user', lazy=True, cascade='all, delete-orphan')
    medication_logs = db.relationship('MedicationLog', backref='user', lazy=True, cascade='all, delete-orphan')
    user_badges = db.relationship('UserBadge', backref='user', lazy=True, cascade='all, delete-orphan')
    
    serialize_rules = ('-password_hash', '-glucose_readings.user', '-food_logs.user', '-exercise_logs.user')

class GlucoseReading(db.Model, SerializerMixin):
    __tablename__ = 'glucose_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Reading Information
    glucose_value = db.Column(db.Float, nullable=False)  # mg/dL
    reading_type = db.Column(SQLEnum('fasting', 'post_meal', 'random', 'bedtime', name='reading_types'))
    measurement_date = db.Column(db.Date, nullable=False)
    measurement_time = db.Column(db.Time, nullable=False)
    
    # Context
    meal_context = db.Column(db.String(200))  # What was eaten
    notes = db.Column(db.Text)
    symptoms = db.Column(db.String(500))  # Any symptoms experienced
    
    # Kenyan-specific context
    traditional_food_consumed = db.Column(db.String(200))  # Traditional Kenyan foods
    seasonal_context = db.Column(db.String(50))  # Which Kenyan season
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class KenyanFood(db.Model, SerializerMixin):
    __tablename__ = 'kenyan_foods'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Names
    name_english = db.Column(db.String(100), nullable=False)
    name_swahili = db.Column(db.String(100), nullable=False)
    name_local = db.Column(db.String(100))  # Other local languages
    
    # Classification
    category = db.Column(SQLEnum('grains', 'vegetables', 'fruits', 'proteins', 'dairy', 'legumes', 'tubers', name='food_categories'))
    subcategory = db.Column(db.String(50))
    
    # Nutritional Information (per 100g)
    calories = db.Column(db.Float)
    carbohydrates_g = db.Column(db.Float)
    protein_g = db.Column(db.Float)
    fat_g = db.Column(db.Float)
    fiber_g = db.Column(db.Float)
    sodium_mg = db.Column(db.Float)
    glycemic_index = db.Column(db.Integer)
    
    # Diabetes Information
    diabetes_friendly = db.Column(db.Boolean, default=False)
    recommended_portion = db.Column(db.String(100))
    
    # Cultural Information
    description_english = db.Column(db.Text)
    description_swahili = db.Column(db.Text)
    cultural_significance = db.Column(db.Text)
    preparation_methods = db.Column(db.Text)
    
    # Seasonal Information
    peak_season = db.Column(db.String(100))
    regional_availability = db.Column(db.Text)  # JSON string of regions
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    food_logs = db.relationship('FoodLog', backref='kenyan_food', lazy=True)

class FoodLog(db.Model, SerializerMixin):
    __tablename__ = 'food_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    kenyan_food_id = db.Column(db.Integer, db.ForeignKey('kenyan_foods.id'))
    
    # Food Information
    food_name = db.Column(db.String(100), nullable=False)
    food_name_swahili = db.Column(db.String(100))
    portion_size = db.Column(db.String(50))
    portion_weight_g = db.Column(db.Float)
    
    # Meal Information
    meal_type = db.Column(SQLEnum('breakfast', 'lunch', 'dinner', 'snack', name='meal_types'))
    meal_date = db.Column(db.Date, nullable=False)
    meal_time = db.Column(db.Time, nullable=False)
    
    # Nutritional Calculation
    calories_consumed = db.Column(db.Float)
    carbs_consumed_g = db.Column(db.Float)
    
    # Context
    cooking_method = db.Column(db.String(100))
    accompaniments = db.Column(db.String(200))  # What was eaten with it
    location_eaten = db.Column(db.String(100))  # Home, restaurant, etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExerciseLog(db.Model, SerializerMixin):
    __tablename__ = 'exercise_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Exercise Information
    exercise_type = db.Column(db.String(100), nullable=False)
    exercise_type_swahili = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer, nullable=False)
    intensity = db.Column(SQLEnum('low', 'moderate', 'high', name='intensity_levels'))
    
    # Traditional Kenyan Activities
    is_traditional_activity = db.Column(db.Boolean, default=False)
    traditional_activity_name = db.Column(db.String(100))  # e.g., "Ohangla dance", "Farm work"
    
    # Context
    exercise_date = db.Column(db.Date, nullable=False)
    exercise_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    # Health Impact
    calories_burned = db.Column(db.Float)
    glucose_before = db.Column(db.Float)
    glucose_after = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MedicationLog(db.Model, SerializerMixin):
    __tablename__ = 'medication_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Medication Information
    medication_name = db.Column(db.String(100), nullable=False)
    medication_type = db.Column(SQLEnum('insulin', 'metformin', 'other_oral', 'injectable', name='medication_types'))
    dosage = db.Column(db.String(50))
    dosage_unit = db.Column(db.String(20))
    
    # Timing
    taken_date = db.Column(db.Date, nullable=False)
    taken_time = db.Column(db.Time, nullable=False)
    scheduled_time = db.Column(db.Time)
    
    # Context
    taken_with_food = db.Column(db.Boolean, default=False)
    meal_context = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    # NHIF Information
    nhif_covered = db.Column(db.Boolean, default=False)
    cost_ksh = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Badge(db.Model, SerializerMixin):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Badge Information
    name_english = db.Column(db.String(100), nullable=False)
    name_swahili = db.Column(db.String(100), nullable=False)
    description_english = db.Column(db.Text)
    description_swahili = db.Column(db.Text)
    
    # Badge Properties
    category = db.Column(SQLEnum('food', 'exercise', 'glucose', 'consistency', 'cultural', name='badge_categories'))
    difficulty = db.Column(SQLEnum('bronze', 'silver', 'gold', 'platinum', name='badge_difficulties'))
    points_value = db.Column(db.Integer, default=0)
    
    # Requirements (JSON string)
    requirements = db.Column(db.Text)  # JSON string of requirements
    
    # Cultural Context
    kenyan_cultural_element = db.Column(db.String(200))  # What Kenyan element it represents
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_badges = db.relationship('UserBadge', backref='badge', lazy=True)

class UserBadge(db.Model, SerializerMixin):
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    
    # Achievement Information
    earned_date = db.Column(db.Date, nullable=False)
    progress_when_earned = db.Column(db.Text)  # JSON string of progress data
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HealthFacility(db.Model, SerializerMixin):
    __tablename__ = 'health_facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    name = db.Column(db.String(200), nullable=False)
    facility_type = db.Column(SQLEnum('national_hospital', 'county_hospital', 'sub_county_hospital', 
                                     'health_center', 'dispensary', 'private_hospital', 'clinic', 
                                     'pharmacy', 'laboratory', name='facility_types'))
    
    # Location
    county = db.Column(db.String(50), nullable=False)
    sub_county = db.Column(db.String(50))
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Contact Information
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(100))
    emergency_contact = db.Column(db.String(15))
    
    # Services (JSON string)
    services_offered = db.Column(db.Text)  # JSON array of services
    diabetes_services = db.Column(db.Text)  # JSON object of diabetes-specific services
    
    # NHIF and Insurance
    nhif_accredited = db.Column(db.Boolean, default=False)
    insurance_accepted = db.Column(db.Text)  # JSON array of accepted insurance
    
    # Operating Information
    operating_hours = db.Column(db.Text)  # JSON object of hours by day
    languages_supported = db.Column(db.Text)  # JSON array of languages
    accessibility_features = db.Column(db.Text)  # JSON array of accessibility features
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CulturalEvent(db.Model, SerializerMixin):
    __tablename__ = 'cultural_events'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Event Information
    name_english = db.Column(db.String(200), nullable=False)
    name_swahili = db.Column(db.String(200), nullable=False)
    event_type = db.Column(SQLEnum('health_awareness', 'national_holiday', 'religious', 'seasonal', name='event_types'))
    
    # Date Information
    event_date = db.Column(db.Date, nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(100))  # e.g., "annual", "monthly"
    
    # Content
    description_english = db.Column(db.Text)
    description_swahili = db.Column(db.Text)
    health_tips = db.Column(db.Text)  # JSON array of health tips
    traditional_foods = db.Column(db.Text)  # JSON array of recommended foods
    
    # Cultural Context
    cultural_significance = db.Column(db.Text)
    regional_variations = db.Column(db.Text)  # JSON object of regional differences
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserProgress(db.Model, SerializerMixin):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Gamification Progress
    total_points = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=1)
    badges_earned = db.Column(db.Integer, default=0)
    
    # Health Progress
    days_logged = db.Column(db.Integer, default=0)
    glucose_readings_count = db.Column(db.Integer, default=0)
    food_logs_count = db.Column(db.Integer, default=0)
    exercise_logs_count = db.Column(db.Integer, default=0)
    
    # Streaks
    current_logging_streak = db.Column(db.Integer, default=0)
    longest_logging_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date)
    
    # Cultural Engagement
    traditional_foods_tried = db.Column(db.Integer, default=0)
    cultural_events_participated = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Association table for many-to-many relationships
user_support_groups = db.Table('user_support_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('support_group_id', db.Integer, db.ForeignKey('support_groups.id'), primary_key=True)
)

class SupportGroup(db.Model, SerializerMixin):
    __tablename__ = 'support_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Group Information
    name_english = db.Column(db.String(200), nullable=False)
    name_swahili = db.Column(db.String(200), nullable=False)
    description_english = db.Column(db.Text)
    description_swahili = db.Column(db.Text)
    
    # Location
    county = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200))
    meeting_venue = db.Column(db.String(200))
    
    # Meeting Information
    meeting_day = db.Column(db.String(50))
    meeting_time = db.Column(db.Time)
    meeting_frequency = db.Column(db.String(50))  # weekly, monthly, etc.
    
    # Contact Information
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(15))
    contact_email = db.Column(db.String(100))
    
    # Group Properties
    group_type = db.Column(SQLEnum('diabetes', 'nutrition', 'exercise', 'general_health', name='group_types'))
    languages_supported = db.Column(db.Text)  # JSON array
    activities_offered = db.Column(db.Text)  # JSON array
    cost = db.Column(db.String(50))  # "Free", "KSh 100", etc.
    
    # Membership
    current_members = db.Column(db.Integer, default=0)
    max_members = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('User', secondary=user_support_groups, backref='support_groups')
