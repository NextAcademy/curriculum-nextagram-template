from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from models.user import User
from flask_assets import Environment, Bundle
from flask_login import LoginManager, current_user
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

login_manager = LoginManager(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images" )

@login_manager.user_loader
def load_user(id):
    return User.get_or_none(id=id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    user = User.get(User.id == current_user.id)
    return render_template('home.html', user=user)
