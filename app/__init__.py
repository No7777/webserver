from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from pymongo import MongoClient
from config import Config

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
emotion_db = MongoClient('mongodb://172.20.111.219:27017/').emotion_db
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from weibo import weibo as weibo_blueprint
    app.register_blueprint(weibo_blueprint)

    from news import news as news_blueprint
    app.register_blueprint(news_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
