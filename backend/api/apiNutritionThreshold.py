from flask import Blueprint, jsonify, request
from .apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getThreshold import NutritionThreshold

# Initialize Flask app
get_nutrition_threshold_bp = Blueprint("get_nutrition_threshold", __name__)

@get_nutrition_threshold_bp.route("/nutrition_threshold", methods=["POST"])
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
