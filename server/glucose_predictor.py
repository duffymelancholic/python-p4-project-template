"""
Glucose Predictor - AI-powered glucose level prediction system
for Kenyan foods and personalized health insights.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import json

from kenyan_foods import get_kenyan_food_database, KenyanFood

@dataclass
class GlucoseReading:
    timestamp: datetime
    glucose_level: float
    meal_context: Optional[str] = None
    food_consumed: Optional[List[str]] = None
    portion_sizes: Optional[List[float]] = None
    exercise_minutes: Optional[int] = None
    stress_level: Optional[int] = None  # 1-10 scale
    sleep_hours: Optional[float] = None

@dataclass
class UserProfile:
    user_id: str
    age: int
    weight_kg: float
    height_cm: float
    diabetes_type: Optional[str] = None  # Type 1, Type 2, Prediabetes, None
    medication: Optional[List[str]] = None
    activity_level: str = "moderate"  # low, moderate, high
    target_glucose_range: Tuple[float, float] = (80, 140)

class GlucosePredictor:
    """AI-powered glucose prediction system with Kenyan food integration"""
    
    def __init__(self):
        self.food_db = get_kenyan_food_database()
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'carbs_g', 'protein_g', 'fat_g', 'fiber_g', 'glycemic_load',
            'portion_size', 'time_since_last_meal', 'exercise_minutes',
            'stress_level', 'sleep_hours', 'age', 'weight_kg', 'bmi'
        ]
        
    def _generate_synthetic_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for the model"""
        np.random.seed(42)
        
        # Generate realistic feature combinations
        data = []
        targets = []
        
        for _ in range(n_samples):
            # Meal composition (realistic Kenyan meal combinations)
            carbs = np.random.uniform(20, 80)  # grams
            protein = np.random.uniform(5, 40)  # grams
            fat = np.random.uniform(2, 25)  # grams
            fiber = np.random.uniform(1, 15)  # grams
            glycemic_load = np.random.uniform(5, 25)
            portion_size = np.random.uniform(100, 400)  # grams
            
            # Timing and lifestyle factors
            time_since_last_meal = np.random.uniform(1, 8)  # hours
            exercise_minutes = np.random.uniform(0, 120)
            stress_level = np.random.randint(1, 11)
            sleep_hours = np.random.uniform(4, 10)
            
            # User characteristics
            age = np.random.uniform(20, 80)
            weight_kg = np.random.uniform(50, 120)
            height_cm = np.random.uniform(150, 190)
            bmi = weight_kg / ((height_cm / 100) ** 2)
            
            features = [
                carbs, protein, fat, fiber, glycemic_load, portion_size,
                time_since_last_meal, exercise_minutes, stress_level,
                sleep_hours, age, weight_kg, bmi
            ]
            
            # Simulate glucose response (simplified model)
            base_glucose = 90 + np.random.normal(0, 10)
            
            # Carbohydrate impact
            carb_impact = (carbs * 2) + (glycemic_load * 1.5)
            
            # Fiber reduces glucose spike
            fiber_effect = -fiber * 2
            
            # Protein has moderate impact
            protein_effect = protein * 0.5
            
            # Exercise reduces glucose
            exercise_effect = -exercise_minutes * 0.3
            
            # Stress increases glucose
            stress_effect = stress_level * 2
            
            # Sleep deprivation increases glucose
            sleep_effect = (8 - sleep_hours) * 3 if sleep_hours < 8 else 0
            
            # Time since last meal affects baseline
            time_effect = -time_since_last_meal * 2
            
            # BMI effect (higher BMI = higher glucose)
            bmi_effect = (bmi - 25) * 1.5 if bmi > 25 else 0
            
            predicted_glucose = (base_glucose + carb_impact + fiber_effect + 
                               protein_effect + exercise_effect + stress_effect + 
                               sleep_effect + time_effect + bmi_effect)
            
            # Add some noise and ensure realistic range
            predicted_glucose += np.random.normal(0, 15)
            predicted_glucose = max(60, min(300, predicted_glucose))
            
            data.append(features)
            targets.append(predicted_glucose)
        
        return np.array(data), np.array(targets)
    
    def train_model(self):
        """Train the glucose prediction model"""
        print("Generating synthetic training data...")
        X, y = self._generate_synthetic_data(2000)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        print("Training glucose prediction model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Model trained successfully!")
        print(f"Training R² score: {train_score:.3f}")
        print(f"Testing R² score: {test_score:.3f}")
        
        self.is_trained = True
    
    def predict_glucose_response(
        self, 
        foods: List[str], 
        portions: List[float],
        user_profile: UserProfile,
        meal_context: Dict = None
    ) -> Dict:
        """Predict glucose response to a meal"""
        
        if not self.is_trained:
            self.train_model()
        
        # Calculate meal nutrition
        food_portions = [(food_id, portion) for food_id, portion in zip(foods, portions)]
        meal_nutrition = self.food_db.calculate_meal_nutrition(food_portions)
        
        # Extract meal context
        context = meal_context or {}
        time_since_last_meal = context.get('time_since_last_meal', 4.0)
        exercise_minutes = context.get('exercise_minutes', 0)
        stress_level = context.get('stress_level', 5)
        sleep_hours = context.get('sleep_hours', 7.5)
        
        # Calculate BMI
        bmi = user_profile.weight_kg / ((user_profile.height_cm / 100) ** 2)
        
        # Prepare features
        features = np.array([[
            meal_nutrition['carbohydrates_g'],
            meal_nutrition['protein_g'],
            meal_nutrition['fat_g'],
            meal_nutrition['fiber_g'],
            meal_nutrition['glycemic_load'],
            sum(portions),  # total portion size
            time_since_last_meal,
            exercise_minutes,
            stress_level,
            sleep_hours,
            user_profile.age,
            user_profile.weight_kg,
            bmi
        ]])
        
        # Scale features and predict
        features_scaled = self.scaler.transform(features)
        predicted_glucose = self.model.predict(features_scaled)[0]
        
        # Get feature importance for explanation
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        # Generate time-series prediction (simplified)
        time_points = [0, 30, 60, 90, 120, 180]  # minutes after meal
        glucose_curve = []
        
        baseline = 95  # Assumed fasting glucose
        peak_time = 60  # Peak at 60 minutes
        
        for t in time_points:
            if t == 0:
                glucose_curve.append(baseline)
            else:
                # Simplified glucose curve
                if t <= peak_time:
                    # Rising phase
                    glucose = baseline + (predicted_glucose - baseline) * (t / peak_time)
                else:
                    # Falling phase
                    decay_factor = np.exp(-(t - peak_time) / 120)
                    glucose = baseline + (predicted_glucose - baseline) * decay_factor
                
                glucose_curve.append(max(baseline, glucose))
        
        return {
            'predicted_peak_glucose': round(predicted_glucose, 1),
            'glucose_curve': {
                'time_minutes': time_points,
                'glucose_levels': [round(g, 1) for g in glucose_curve]
            },
            'meal_nutrition': meal_nutrition,
            'risk_assessment': self._assess_glucose_risk(predicted_glucose, user_profile),
            'recommendations': self._generate_recommendations(
                predicted_glucose, meal_nutrition, user_profile
            ),
            'feature_importance': feature_importance
        }
    
    def _assess_glucose_risk(self, predicted_glucose: float, user_profile: UserProfile) -> Dict:
        """Assess the risk level of predicted glucose"""
        target_min, target_max = user_profile.target_glucose_range
        
        if predicted_glucose < target_min:
            risk_level = "low"
            message = "Glucose may be too low. Consider adding healthy carbs."
        elif predicted_glucose <= target_max:
            risk_level = "normal"
            message = "Glucose levels should be within target range."
        elif predicted_glucose <= target_max + 40:
            risk_level = "elevated"
            message = "Glucose may be elevated. Consider reducing portions or adding exercise."
        else:
            risk_level = "high"
            message = "High glucose risk. Consider meal modifications."
        
        return {
            'risk_level': risk_level,
            'message': message,
            'target_range': user_profile.target_glucose_range
        }
    
    def _generate_recommendations(
        self, 
        predicted_glucose: float, 
        meal_nutrition: Dict, 
        user_profile: UserProfile
    ) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        target_min, target_max = user_profile.target_glucose_range
        
        if predicted_glucose > target_max:
            recommendations.extend([
                "Consider reducing portion sizes",
                "Add more fiber-rich vegetables like sukuma wiki",
                "Take a 10-15 minute walk after eating",
                "Drink plenty of water"
            ])
            
            if meal_nutrition['carbohydrates_g'] > 60:
                recommendations.append("Reduce high-carb foods like ugali or rice")
            
            if meal_nutrition['fiber_g'] < 10:
                recommendations.append("Add more high-fiber foods like githeri")
        
        elif predicted_glucose < target_min:
            recommendations.extend([
                "Consider adding healthy carbohydrates",
                "Include fruits like baobab fruit",
                "Ensure adequate portion sizes"
            ])
        
        # General diabetes-friendly recommendations
        if user_profile.diabetes_type:
            recommendations.extend([
                "Monitor glucose levels regularly",
                "Stay consistent with meal timing",
                "Consider pairing carbs with protein"
            ])
        
        return recommendations
    
    def analyze_glucose_patterns(self, readings: List[GlucoseReading]) -> Dict:
        """Analyze patterns in glucose readings"""
        if not readings:
            return {"error": "No readings provided"}
        
        df = pd.DataFrame([
            {
                'timestamp': r.timestamp,
                'glucose': r.glucose_level,
                'hour': r.timestamp.hour,
                'day_of_week': r.timestamp.weekday()
            }
            for r in readings
        ])
        
        patterns = {
            'average_glucose': df['glucose'].mean(),
            'glucose_variability': df['glucose'].std(),
            'time_in_range': len(df[(df['glucose'] >= 80) & (df['glucose'] <= 140)]) / len(df) * 100,
            'peak_hours': df.groupby('hour')['glucose'].mean().idxmax(),
            'lowest_hours': df.groupby('hour')['glucose'].mean().idxmin(),
            'weekend_vs_weekday': {
                'weekday_avg': df[df['day_of_week'] < 5]['glucose'].mean(),
                'weekend_avg': df[df['day_of_week'] >= 5]['glucose'].mean()
            }
        }
        
        return patterns
    
    def get_food_impact_score(self, food_id: str, portion_g: float = 100) -> Dict:
        """Get the predicted glucose impact of a specific food"""
        food = self.food_db.get_food_by_id(food_id)
        if not food:
            return {"error": "Food not found"}
        
        # Create a sample user profile for scoring
        sample_user = UserProfile(
            user_id="sample",
            age=35,
            weight_kg=70,
            height_cm=170
        )
        
        prediction = self.predict_glucose_response(
            foods=[food_id],
            portions=[portion_g],
            user_profile=sample_user
        )
        
        return {
            'food_name': food.name_english,
            'swahili_name': food.name_swahili,
            'portion_g': portion_g,
            'predicted_glucose_impact': prediction['predicted_peak_glucose'] - 95,  # Subtract baseline
            'diabetes_friendly': food.diabetes_friendly,
            'glycemic_index': food.nutritional_info.glycemic_index,
            'recommendations': food.preparation_tips
        }

# Global instance
glucose_predictor = GlucosePredictor()

def get_glucose_predictor() -> GlucosePredictor:
    """Get the global glucose predictor instance"""
    return glucose_predictor
