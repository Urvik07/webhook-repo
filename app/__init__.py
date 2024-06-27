from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
    mongo.init_app(app)
    
    from app.webhook.routes import webhook
    app.register_blueprint(webhook)
    
    return app