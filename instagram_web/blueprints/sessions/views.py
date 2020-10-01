from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user
from app import app
from instagram_web.util.google_oauth import oauth

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
            flash(u'ye, you is in', 'success')
            return redirect(url_for('users.index'))
        else:
            flash(u'right name, wrong pass', 'danger')
            return render_template('sessions/new.html')
    else:
        flash(u"bruh, you don't exist", 'warning')
        return render_template('sessions/new.html')


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google')
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)

    if user:
        login_user(user)
        return redirect(url_for('users.edit', id=current_user.id))
    else:
        flash('That google email is not registered on Nextagram. soz.')
        return redirect(url_for('users.index'))
