from s3_uploader import *
from app import app
from flask import render_template, abort, flash, request, redirect, url_for
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.follower_following.views import follower_following_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from models.user import User
from models.images import Image
import os
import config
from app import oauth

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follower_following_blueprint,
                       url_prefix="/follower_following")

csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

oauth.init_app(app)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/home")
def home():
    images = Image.select().order_by(Image.created_at.desc())
    return render_template('home.html', images=images)


@app.route("/")
def main():
    return render_template('main.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)
