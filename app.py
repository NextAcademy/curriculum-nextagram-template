import os
import config
from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from models.base_model import db
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect()
csrf.init_app(app)
app.secret_key = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.new"
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "info"


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
