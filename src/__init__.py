import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_pyfile("config.py")

    
    from src import routes
    app.register_blueprint(routes.book_api)

    db.init_app(app)
    migrate.init_app(app, db)
    
    # ensure the instance folder exists


    # try:
    #     from src import model
    #     from src import routes
    #     # app.app_context().push()
    #     app.register_blueprint(routes.book_api)
    #     print("dotted")
    # except Exception as e:
    #     pass
    from src.model import Book
    
    return app

