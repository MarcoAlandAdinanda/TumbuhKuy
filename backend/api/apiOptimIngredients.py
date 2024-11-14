from flask import Blueprint, jsonify, request
import numpy as np
from .apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getIngredients import IngredientsGenerator

# Initialize Flask app
optimized_ingredients_bp = Blueprint("optimized_ingredients", __name__)

@optimized_ingredients_bp.route("/optimized_ingredients", methods=["POST"])
def optimized_ingredients():
    # Get JSON data from the request
    data = request.get_json()

    # Check if all required parameters are present
    required_params = ["is_female", "year_age", "mode", "massa_tubuh", "max_price"]
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify(error=f"Missing required parameters: {', '.join(missing_params)}"), 400

    # Extract parameters from JSON
    is_female = data["is_female"]
    year_age = data["year_age"]
    mode = data["mode"]
    massa_tubuh = data["massa_tubuh"]
    max_price = data["max_price"]

    # Initialize and configure the IngredientsGenerator
    ingredient_gen = IngredientsGenerator()
    ingredient_gen.set_info(is_female=is_female, year_age=year_age, mode=mode, massa_tubuh=massa_tubuh)
    ingredient_gen.nutrition_optim(max_price=max_price)

    optimized_ingredients: list = ingredient_gen.optimized_ingredients

    message: dict = {"optimized_ingredients": optimized_ingredients, # list of optimized ingredients
                     "optim_total_nutrition": convert_to_serializable(ingredient_gen.optim_total_nutrition), # dictionary of sum of optimized ingredients
                     "user_threshold": ingredient_gen.user_threshold} # dictionary of user threshold
    # Return JSON response
    return jsonify(optimized=message)

def convert_to_serializable(obj):
    """Convert numpy int64 and other non-serializable types to Python-native types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_serializable(i) for i in obj)
    return obj