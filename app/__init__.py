# app/__init__.py
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from instance.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app import models

    with app.app_context():
        logging.info(f"Database URI is {app.config['SQLALCHEMY_DATABASE_URI']}")
        logging.info("Creating all tables in the database.")
        db.create_all()
        logging.info("Tables created successfully.")

    from app.auth import auth_bp
    from app.routes import routes_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(routes_bp, url_prefix='/')

    return app
