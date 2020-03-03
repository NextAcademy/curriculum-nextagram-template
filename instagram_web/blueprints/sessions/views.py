from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user
from app import app

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)


@sessions_blueprint.route('/', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@sessions_blueprint.route('/sign_in', methods=['POST'])
def sign_in():
    username = request.form.get('username')
    password = request.form.get('password')
    if User.get_or_none(User.username == username):
        user = User.get(User.username == username)
        hashed_pass = user.password
        if check_password_hash(hashed_pass, password):
            load_user(user.id)
            login_user(user)
            flash('ye, you is in', 'notice')
            return redirect(url_for('users.index'))
        else:
            flash('right name, wrong pass', 'error')
            return render_template('sessions/new.html')
    else:
        flash("bruh, you don't exist", 'warning')
        return render_template('sessions/new.html')


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions.new'))
