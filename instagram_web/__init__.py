from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
import os
from models.user import User

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")

csrf = CsrfProtect(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

@app.errorhandler(400)
def internal_server_error(e):
    return render_template('400.html'), 400

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.login"
login_manager.login_message = u"Please login to access this function."

@login_manager.user_loader
def load_user(id):
    return User.get_or_none(id=id)

@app.route("/")
def home():
    return render_template('home.html')

