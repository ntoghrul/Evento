from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
DB_NAME = "database.db"
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KAKAVA123SKD'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'evvennto@gmail.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'evvennto@gmail.com' 
    app.config['MAIL_PASSWORD'] = 'ywsmdaqxpknrrnfg' 
    db.init_app(app)
    mail.init_app(app)

    from views import views

    app.register_blueprint(views, url_prefix='/')

    from models import User,OrganizerEvent,Event,Ticket

    create_database(app)


    login_manager.login_view = 'views.home'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
