from .apiClassify import classify_status_bp
from .apiIngredientNutri import get_ingredient_info_bp
from .apiNutritionThreshold import get_nutrition_threshold_bp
from .apiOptimIngredients import optimized_ingredients_bp
from .apiRecipes import generate_recipes_bp

def register_blueprints(app):
    app.register_blueprint(classify_status_bp)
    app.register_blueprint(get_ingredient_info_bp)
    app.register_blueprint(get_nutrition_threshold_bp)
    app.register_blueprint(optimized_ingredients_bp)
    app.register_blueprint(generate_recipes_bp)