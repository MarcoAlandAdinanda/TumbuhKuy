from flask import Flask, jsonify, request
from apiUtils import set_scr_path
set_scr_path()  # set system path to scripts directory

from getStatus import StatusClassifier

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

if __name__ == "__main__":
    app.run()
