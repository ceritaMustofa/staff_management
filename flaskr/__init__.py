import os
from flask import Flask
from flaskr.model import db
from flask_migrate import Migrate
from flaskr.auth import auth

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        
    # Ensure the instance folder exists
    
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return 'Hello world!'
    
    app.register_blueprint(auth)
    
    return app