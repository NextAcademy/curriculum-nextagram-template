from app import app
import os
from flask import render_template, redirect, flash, url_for
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.comments.views import comments_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.payments.views import payments_blueprint
from instagram_web.blueprints.fan_idol.views import fan_idol_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user
from instagram_web.util.google_oauth import oauth

csrf = CSRFProtect()
csrf.init_app(app)
oauth.init_app(app)

assets = Environment(app)
assets.register(bundles)



app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(payments_blueprint, url_prefix="/payments")
app.register_blueprint(comments_blueprint, url_prefix="/comments")
app.register_blueprint(fan_idol_blueprint, url_prefix="/fan_idol")

# app.config['TRAP_HTTP_EXCEPTIONS'] = True

# @app.errorhandler(Exception)
# def handle_error(e):
#     if e.code == 404:
#         return render_template('404.html'), 404
#     elif e.code == 500:
#         return render_template('505.html'), 500
#     else:
#         return str(e.code) + ": Something went wrong"

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('images.index'))
    else:
        flash("You are not logged in", "info")
        return redirect(url_for('sessions.new'))
