from flask import Flask
from flask_cors import CORS
from . import register_blueprints

app = Flask(__name__)
CORS(app)

# Register the blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run()
