from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    # Configure the MongoDB connection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
    
    # Initialize the PyMongo instance with the Flask app
    mongo.init_app(app)
    
    # Import and register the webhook blueprint
    from app.webhook.routes import webhook
    app.register_blueprint(webhook)
    
    return app
