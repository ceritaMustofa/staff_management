import os
from datetime import timedelta
from flask import Flask
from flaskr.model import db
from flask_migrate import Migrate
from flaskr.auth import auth, jwt
from flaskr.dashboard import dashboard
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    ACCESS_EXPIRES = timedelta(hours=1)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
        )
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        
    
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    jwt.init_app(app)
    cors_allow_origin = {
        "origins": "http://localhost:8080"
    }
    
    CORS(app, resources={r"/*": {"origins": cors_allow_origin}})
    
    
    
    
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    
    
    return app