"""
Comprehensive database of traditional Kenyan foods
with nutritional information and health insights for diabetes management.
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class FoodCategory(Enum):
    STAPLES = "staples"
    VEGETABLES = "vegetables"
    PROTEINS = "proteins"
    FRUITS = "fruits"
    BEVERAGES = "beverages"
    SNACKS = "snacks"
    TRADITIONAL = "traditional"

class GlycemicIndex(Enum):
    LOW = "low"      # GI < 55
    MEDIUM = "medium" # GI 55-70
    HIGH = "high"    # GI > 70

@dataclass
class NutritionalInfo:
    calories_per_100g: float
    carbohydrates_g: float
    protein_g: float
    fat_g: float
    fiber_g: float
    sugar_g: float
    sodium_mg: float
    glycemic_index: int
    glycemic_load: float

@dataclass
class KenyanFood:
    id: str
    name_english: str
    name_swahili: str
    name_local: Optional[str]
    category: FoodCategory
    nutritional_info: NutritionalInfo
    description_english: str
    description_swahili: str
    health_benefits: List[str]
    diabetes_friendly: bool
    preparation_tips: List[str]
    serving_size_g: float
    common_combinations: List[str]
    seasonal_availability: List[str]
    regions: List[str]

class KenyanFoodDatabase:
    """Comprehensive database of Kenyan foods with health insights"""
    
    def __init__(self):
        self.foods = self._initialize_database()
        self.food_index = {food.id: food for food in self.foods}
        self.name_index = self._create_name_index()
    
    def _initialize_database(self) -> List[KenyanFood]:
        """Initialize the database with comprehensive Kenyan food data"""
        return [
            # STAPLES
            KenyanFood(
                id="ugali",
                name_english="Ugali",
                name_swahili="Ugali",
                name_local="Posho",
                category=FoodCategory.STAPLES,
                nutritional_info=NutritionalInfo(
                    calories_per_100g=112,
                    carbohydrates_g=24.0,
                    protein_g=2.3,
                    fat_g=0.4,
                    fiber_g=1.2,
                    sugar_g=0.2,
                    sodium_mg=2,
                    glycemic_index=72,
                    glycemic_load=17.3
                ),
                description_english="Traditional cornmeal staple, served with vegetables and meat",
                description_swahili="Chakula cha msingi kinachotengenezwa na unga wa mahindi",
                health_benefits=[
                    "Good source of energy",
                    "Contains some protein",
                    "Gluten-free option"
                ],
                diabetes_friendly=False,
                preparation_tips=[
                    "Serve smaller portions",
                    "Combine with high-fiber vegetables",
                    "Add protein to slow glucose absorption"
                ],
                serving_size_g=150.0,
                common_combinations=["Sukuma wiki", "Nyama", "Mboga"],
                seasonal_availability=["All year"],
                regions=["All Kenya"]
            ),
            
            KenyanFood(
                id="githeri",
                name_english="Githeri",
                name_swahili="Githeri",
                name_local="Mixed beans and maize",
                category=FoodCategory.STAPLES,
                nutritional_info=NutritionalInfo(
                    calories_per_100g=130,
                    carbohydrates_g=22.0,
                    protein_g=6.5,
                    fat_g=1.2,
                    fiber_g=5.8,
                    sugar_g=2.1,
                    sodium_mg=8,
                    glycemic_index=45,
                    glycemic_load=9.9
                ),
                description_english="Traditional mix of boiled maize and beans",
                description_swahili="Mchanganyiko wa mahindi na maharagwe",
                health_benefits=[
                    "High in protein and fiber",
                    "Low glycemic index",
                    "Rich in minerals",
                    "Helps control blood sugar"
                ],
                diabetes_friendly=True,
                preparation_tips=[
                    "Soak beans overnight",
                    "Add vegetables for extra nutrients",
                    "Use minimal oil"
                ],
                serving_size_g=200.0,
                common_combinations=["Avocado", "Sukuma wiki", "Stew"],
                seasonal_availability=["All year"],
                regions=["Central Kenya", "Eastern Kenya"]
            ),

            # VEGETABLES
            KenyanFood(
                id="sukuma_wiki",
                name_english="Collard Greens",
                name_swahili="Sukuma Wiki",
                name_local="Kale",
                category=FoodCategory.VEGETABLES,
                nutritional_info=NutritionalInfo(
                    calories_per_100g=35,
                    carbohydrates_g=7.3,
                    protein_g=3.3,
                    fat_g=0.6,
                    fiber_g=3.6,
                    sugar_g=1.5,
                    sodium_mg=38,
                    glycemic_index=15,
                    glycemic_load=1.1
                ),
                description_english="Popular leafy green vegetable, often sautéed with onions",
                description_swahili="Mboga za majani yanayoliwa sana Kenya",
                health_benefits=[
                    "Very low glycemic index",
                    "High in vitamins A, C, K",
                    "Rich in antioxidants",
                    "Supports blood sugar control"
                ],
                diabetes_friendly=True,
                preparation_tips=[
                    "Don't overcook to retain nutrients",
                    "Add minimal oil",
                    "Combine with tomatoes and onions"
                ],
                serving_size_g=100.0,
                common_combinations=["Ugali", "Rice", "Chapati"],
                seasonal_availability=["All year"],
                regions=["All Kenya"]
            ),

            # PROTEINS
            KenyanFood(
                id="tilapia",
                name_english="Tilapia Fish",
                name_swahili="Samaki wa Tilapia",
                name_local="Ngege",
                category=FoodCategory.PROTEINS,
                nutritional_info=NutritionalInfo(
                    calories_per_100g=128,
                    carbohydrates_g=0.0,
                    protein_g=26.0,
                    fat_g=2.7,
                    fiber_g=0.0,
                    sugar_g=0.0,
                    sodium_mg=52,
                    glycemic_index=0,
                    glycemic_load=0.0
                ),
                description_english="Fresh water fish from Lake Victoria",
                description_swahili="Samaki wa maji baridi kutoka Ziwa Victoria",
                health_benefits=[
                    "High quality protein",
                    "No carbohydrates",
                    "Rich in omega-3 fatty acids",
                    "Excellent for diabetes"
                ],
                diabetes_friendly=True,
                preparation_tips=[
                    "Grill or steam instead of frying",
                    "Season with herbs and spices",
                    "Serve with vegetables"
                ],
                serving_size_g=150.0,
                common_combinations=["Ugali", "Rice", "Vegetables"],
                seasonal_availability=["All year"],
                regions=["Western Kenya", "Nyanza"]
            ),

            # FRUITS
            KenyanFood(
                id="baobab_fruit",
                name_english="Baobab Fruit",
                name_swahili="Tunda la Mbuyu",
                name_local="Mbuyu",
                category=FoodCategory.FRUITS,
                nutritional_info=NutritionalInfo(
                    calories_per_100g=162,
                    carbohydrates_g=38.0,
                    protein_g=2.3,
                    fat_g=0.3,
                    fiber_g=44.5,
                    sugar_g=38.0,
                    sodium_mg=1,
                    glycemic_index=35,
                    glycemic_load=13.3
                ),
                description_english="Superfruit from the iconic baobab tree",
                description_swahili="Tunda kutoka mti wa mbuyu",
                health_benefits=[
                    "Extremely high in fiber",
                    "Rich in vitamin C",
                    "Contains antioxidants",
                    "Helps regulate blood sugar"
                ],
                diabetes_friendly=True,
                preparation_tips=[
                    "Eat in moderation due to natural sugars",
                    "Mix with water to make drink",
                    "Combine with other low-GI foods"
                ],
                serving_size_g=50.0,
                common_combinations=["Water", "Porridge", "Smoothies"],
                seasonal_availability=["Dry season"],
                regions=["Eastern Kenya", "Northern Kenya"]
            ),

            # TRADITIONAL DISHES
            KenyanFood(
                id="mukimo",
                name_english="Mukimo",
                name_swahili="Mukimo",
                name_local="Irio",
                category=FoodCategory.TRADITIONAL,
                nutritional_info=NutritionalInfo(
                    calories_per_100g=95,
                    carbohydrates_g=18.0,
                    protein_g=3.2,
                    fat_g=1.8,
                    fiber_g=4.2,
                    sugar_g=2.5,
                    sodium_mg=15,
                    glycemic_index=52,
                    glycemic_load=9.4
                ),
                description_english="Traditional mashed mixture of potatoes, maize, beans and greens",
                description_swahili="Mchanganyiko wa viazi, mahindi, maharagwe na mboga",
                health_benefits=[
                    "Balanced macronutrients",
                    "High in fiber",
                    "Contains complete proteins",
                    "Moderate glycemic index"
                ],
                diabetes_friendly=True,
                preparation_tips=[
                    "Use more vegetables, less potato",
                    "Add minimal fat",
                    "Include plenty of greens"
                ],
                serving_size_g=180.0,
                common_combinations=["Meat stew", "Vegetables", "Soup"],
                seasonal_availability=["All year"],
                regions=["Central Kenya", "Kikuyu community"]
            )
        ]
    
    def _create_name_index(self) -> Dict[str, str]:
        """Create index for searching by name"""
        index = {}
        for food in self.foods:
            # Index by English name
            index[food.name_english.lower()] = food.id
            # Index by Swahili name
            index[food.name_swahili.lower()] = food.id
            # Index by local name if available
            if food.name_local:
                index[food.name_local.lower()] = food.id
        return index
    
    def get_food_by_id(self, food_id: str) -> Optional[KenyanFood]:
        """Get food by ID"""
        return self.food_index.get(food_id)
    
    def search_foods(self, query: str) -> List[KenyanFood]:
        """Search foods by name"""
        query = query.lower()
        results = []
        
        for food in self.foods:
            if (query in food.name_english.lower() or 
                query in food.name_swahili.lower() or
                (food.name_local and query in food.name_local.lower())):
                results.append(food)
        
        return results
    
    def get_foods_by_category(self, category: FoodCategory) -> List[KenyanFood]:
        """Get all foods in a category"""
        return [food for food in self.foods if food.category == category]
    
    def get_diabetes_friendly_foods(self) -> List[KenyanFood]:
        """Get all diabetes-friendly foods"""
        return [food for food in self.foods if food.diabetes_friendly]
    
    def get_low_gi_foods(self) -> List[KenyanFood]:
        """Get foods with low glycemic index (< 55)"""
        return [food for food in self.foods 
                if food.nutritional_info.glycemic_index < 55]
    
    def get_seasonal_foods(self, month: str) -> List[KenyanFood]:
        """Get foods available in a specific month"""
        return [food for food in self.foods 
                if month in food.seasonal_availability or 
                "All year" in food.seasonal_availability]
    
    def get_regional_foods(self, region: str) -> List[KenyanFood]:
        """Get foods common in a specific region"""
        return [food for food in self.foods 
                if region in food.regions or "All Kenya" in food.regions]
    
    def calculate_meal_nutrition(self, food_portions: List[Tuple[str, float]]) -> Dict:
        """Calculate total nutrition for a meal
        Args:
            food_portions: List of (food_id, portion_size_g) tuples
        """
        total_nutrition = {
            'calories': 0,
            'carbohydrates_g': 0,
            'protein_g': 0,
            'fat_g': 0,
            'fiber_g': 0,
            'sugar_g': 0,
            'sodium_mg': 0,
            'glycemic_load': 0
        }
        
        for food_id, portion_g in food_portions:
            food = self.get_food_by_id(food_id)
            if food:
                multiplier = portion_g / 100.0  # Nutrition is per 100g
                nutrition = food.nutritional_info
                
                total_nutrition['calories'] += nutrition.calories_per_100g * multiplier
                total_nutrition['carbohydrates_g'] += nutrition.carbohydrates_g * multiplier
                total_nutrition['protein_g'] += nutrition.protein_g * multiplier
                total_nutrition['fat_g'] += nutrition.fat_g * multiplier
                total_nutrition['fiber_g'] += nutrition.fiber_g * multiplier
                total_nutrition['sugar_g'] += nutrition.sugar_g * multiplier
                total_nutrition['sodium_mg'] += nutrition.sodium_mg * multiplier
                total_nutrition['glycemic_load'] += nutrition.glycemic_load * multiplier
        
        return total_nutrition
    
    def get_food_recommendations(self, user_preferences: Dict) -> List[KenyanFood]:
        """Get personalized food recommendations"""
        recommendations = []
        
        # Filter by dietary restrictions
        candidate_foods = self.foods
        
        if user_preferences.get('diabetes_friendly', False):
            candidate_foods = [f for f in candidate_foods if f.diabetes_friendly]
        
        if user_preferences.get('max_gi'):
            max_gi = user_preferences['max_gi']
            candidate_foods = [f for f in candidate_foods 
                             if f.nutritional_info.glycemic_index <= max_gi]
        
        if user_preferences.get('region'):
            region = user_preferences['region']
            candidate_foods = [f for f in candidate_foods 
                             if region in f.regions or "All Kenya" in f.regions]
        
        if user_preferences.get('category'):
            category = FoodCategory(user_preferences['category'])
            candidate_foods = [f for f in candidate_foods if f.category == category]
        
        return candidate_foods[:10]  # Return top 10 recommendations
    
    def to_dict(self) -> Dict:
        """Convert database to dictionary for JSON serialization"""
        return {
            'foods': [asdict(food) for food in self.foods],
            'categories': [cat.value for cat in FoodCategory],
            'total_foods': len(self.foods)
        }

# Global instance
kenyan_food_db = KenyanFoodDatabase()

def get_kenyan_food_database() -> KenyanFoodDatabase:
    """Get the global Kenyan food database instance"""
    return kenyan_food_db
