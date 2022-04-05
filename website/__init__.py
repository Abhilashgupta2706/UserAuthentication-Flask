from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DA_NAME = 'userdatabase.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'encrypt or secure the cookies and session data related to our website'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DA_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    return app


def create_database(app):
    if not path.exists(f'website/{DA_NAME}'):
        db.create_all(app=app)
        print('Database created...')
