from flask import Flask, jsonify, request
from apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getIngredients import IngredientsGenerator

# Initialize Flask app
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()