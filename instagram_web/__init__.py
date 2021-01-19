from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'),403

@app.route("/")
def home():
    return render_template('home.html')
