from flask import Flask
from . import register_blueprints

app = Flask(__name__)

# Register the blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run()
