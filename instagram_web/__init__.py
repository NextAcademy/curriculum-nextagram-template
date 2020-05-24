from app import app
from flask import render_template, redirect, url_for
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.imgs.views import imgs_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager, current_user
from models.user import User
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(imgs_blueprint, url_prefix="/imgs")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")
login_manager = LoginManager()
login_manager.init_app(app)

oauth.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def internal_server_error(e):
    return render_template('404.html'), 401


@app.errorhandler(400)
def internal_server_error(e):
    return render_template('404.html'), 400


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('users.user_profile', id=current_user.id))

    return render_template('home.html')
