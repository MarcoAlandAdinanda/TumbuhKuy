from flask import Flask, jsonify
from flask_cors import CORS
from . import register_blueprints

app = Flask(__name__)
CORS(app)

# Register the blueprints
register_blueprints(app)

# 404 Not Found error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

# 500 Internal Server Error handler
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "An unexpected error occurred"}), 500

# Define a sample route
@app.route('/')
def home():
    return jsonify({"message": "Server is running!"})

if __name__ == '__main__':
    app.run()
