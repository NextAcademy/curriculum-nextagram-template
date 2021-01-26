from app import app
from flask import Flask, Blueprint, render_template, request, redirect
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from instagram_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(donations_blueprint, url_prefix="/images")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    users = User.select()
    return render_template('home.html', users=users)
