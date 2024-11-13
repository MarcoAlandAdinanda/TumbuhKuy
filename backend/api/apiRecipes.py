from flask import Blueprint, jsonify, request
from .apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getIngredients import IngredientsGenerator
from getRecipes import RecipesGenerator

# Initialize Flask app
generate_recipes_bp = Blueprint("generate_recipes", __name__)

@generate_recipes_bp.route("/generate_recipes", methods=["POST"])
def generate_recipes():
    # Get JSON data from the request
    data = request.get_json()

    # Check if required parameters are present
    required_params = ["is_female", "year_age", "month_age", "mode", "max_price", "recipe_year_age"]
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify(error=f"Missing required parameters: {', '.join(missing_params)}"), 400

    # Extract common parameters
    is_female = data["is_female"]
    year_age = data["year_age"]
    month_age = data["month_age"]
    mode = data["mode"]
    max_price = data["max_price"]
    recipe_year_age = data["recipe_year_age"]

    # Check mode-specific parameters
    if mode.lower() == "gizi":
        if "massa_tubuh" not in data:
            return jsonify(error="Missing required parameter for gizi mode: massa_tubuh"), 400
        massa_tubuh = data["massa_tubuh"]
        tinggi_badan = None  # Not needed for gizi mode
    elif mode.lower() == "stunting":
        if "tinggi_badan" not in data:
            return jsonify(error="Missing required parameter for stunting mode: tinggi_badan"), 400
        tinggi_badan = data["tinggi_badan"]
        massa_tubuh = None  # Not needed for stunting mode
    else:
        return jsonify(error="Invalid mode. Choose 'gizi' or 'stunting'."), 400

    # Generate optimized ingredients
    ingredients_gen = IngredientsGenerator()
    ingredients_gen.set_info(
        is_female=is_female, 
        year_age=year_age, 
        month_age=month_age, 
        mode=mode, 
        massa_tubuh=massa_tubuh, 
        tinggi_badan=tinggi_badan
    )
    ingredients_gen.nutrition_optim(max_price=max_price, display=False)
    optimized_ingredients = ingredients_gen.optimized_ingredients

    # Generate recipes based on optimized ingredients
    recipes_gen = RecipesGenerator()
    recipes = recipes_gen.get_recipes(ingredients=optimized_ingredients, year_age=recipe_year_age)

    # Return the recipes and their count as JSON
    return jsonify(recipe_count=len(recipes), recipes=recipes)

if __name__ == "__main__":
    app.run()
