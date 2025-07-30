from flask import Flask
from app.routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = 'f9b3c0e9a16e47b197c8e1c913a4f2fd'
    app.register_blueprint(main_blueprint)
    return app
