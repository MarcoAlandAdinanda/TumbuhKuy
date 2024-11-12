from flask import Flask, jsonify, request
from apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getRawIngredients import IngredientsData

# Initialize Flask app
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()