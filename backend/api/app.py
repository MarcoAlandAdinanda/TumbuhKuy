from flask import Flask, jsonify, request
from apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getStatus import StatusClassifier
from getRawIngredients import IngredientsData
from getThreshold import NutritionThreshold
from getIngredients import IngredientsGenerator
from getRecipes import RecipesGenerator

# Initialize Flask app
app = Flask(__name__)

@app.route("/classify_status", methods=["POST"])
def classify_status():
    # Get JSON data from the request
    data = request.get_json()

    # Check if required parameters are present
    required_params = ["is_female", "year_age", "month_age", "mode", "massa_tubuh", "tinggi_badan"]
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify(error=f"Missing required parameters: {', '.join(missing_params)}"), 400

    # Extract parameters
    is_female = data["is_female"]
    year_age = data["year_age"]
    month_age = data["month_age"]
    mode = data["mode"]
    # massa_tubuh = data["massa_tubuh"]
    # tinggi_badan = data["tinggi_badan"]


    # Optional parameters depending on classification mode
    if mode.lower() == "gizi":
        if "massa_tubuh" not in data:
            return jsonify(error="Missing required parameter for stunting: massa_tubuh"), 400
        massa_tubuh = data["massa_tubuh"]
    elif mode.lower() == "stunting":
        if "tinggi_badan" not in data:
            return jsonify(error="Missing required parameter for gizi: tinggi_badan"), 400
        tinggi_badan = data["tinggi_badan"]
    else:
        return jsonify(error="Invalid classification mode. Choose 'stunting' or 'gizi'."), 400

    # Initialize the classifier and set user information
    classifier = StatusClassifier()
    classifier.set_category(is_female=is_female, year_age=year_age, month_age=month_age)

    # Perform classification based on the mode
    if mode.lower() == "stunting":
        classification = classifier.get_classification(mode=mode, tinggi_tubuh=tinggi_badan)
    else:  # mode is "gizi"
        classification = classifier.get_classification(mode=mode, massa_tubuh=massa_tubuh)

    # Return the classification result as JSON
    return jsonify(classification=classification)

@app.route("/ingredient_info", methods=["POST"])
def get_ingredient_info():
    # Get JSON data from the request
    data = request.get_json()

    # Check if the required parameter 'ingredient_name' is present
    if "ingredient_name" not in data:
        return jsonify(error="Missing required parameter: ingredient_name"), 400

    # Extract the ingredient name from JSON data
    ingredient_name = data["ingredient_name"]
        
    # Initialize IngredientsData and retrieve information
    ingredient_data = IngredientsData()
    ingredient_info = ingredient_data.get_info(ingredient_name)

    # Return the ingredient information in JSON format
    return jsonify(ingredient_info=ingredient_info)

@app.route("/nutrition_threshold", methods=["POST"])
def get_nutrition_threshold():
    # Get JSON data from the request
    data = request.get_json()

    # Check if required parameters are present
    required_params = ["is_female", "month_age", "year_age"]
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify(error=f"Missing required parameters: {', '.join(missing_params)}"), 400

    # Extract parameters from JSON
    is_female = data["is_female"]
    month_age = data["month_age"]
    year_age = data["year_age"]

    # Initialize NutritionThreshold and retrieve threshold data
    boundaries = NutritionThreshold()
    threshold = boundaries.get_threshold(is_female=is_female, month_age=month_age, year_age=year_age)

    # Return the threshold data as JSON
    return jsonify(threshold=threshold)

@app.route("/optimized_ingredients", methods=["POST"])
def index():
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

    # Return JSON response
    return jsonify(message=optimized_ingredients)

@app.route("/generate_recipes", methods=["POST"])
def generate_recipes():
    # Get JSON data from the request
    data = request.get_json()

    # Check if required parameters are present
    required_params = ["is_female", "year_age", "month_age", "mode", "max_price"]#, "recipe_year_age"]
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify(error=f"Missing required parameters: {', '.join(missing_params)}"), 400

    # Extract common parameters
    is_female = data["is_female"]
    year_age = data["year_age"]
    month_age = data["month_age"]
    mode = data["mode"]
    max_price = data["max_price"]
    # recipe_year_age = data["recipe_year_age"]

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
    recipes = recipes_gen.get_recipes(ingredients=optimized_ingredients, year_age=year_age)

    # Return the recipes and their count as JSON
    return jsonify(recipe_count=len(recipes), recipes=recipes)

if __name__ == "__main__":
    app.run()