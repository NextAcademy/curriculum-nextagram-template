from app import app
from flask import render_template, redirect, url_for
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from flask_login import current_user
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    return render_template('home.html')
