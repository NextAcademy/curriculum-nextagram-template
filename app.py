import os
import config
from flask import Flask, session, redirect, url_for, escape, request, render_template
from models.base_model import db
from models.user import User
from flask_wtf.csrf import CSRFProtect
from flask_login import login_required, LoginManager, logout_user, current_user

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')
login_manager = LoginManager()

login_manager.init_app(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('home.html')
    
@app.route('/logout')
@login_required
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('index'))

