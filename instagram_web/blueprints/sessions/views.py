from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from instagram_web.util.google_oauth import oauth


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/sessions')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template("new.html")


@sessions_blueprint.route('/', methods=['POST'])
def create():
    password = request.form.get('password')
    username = request.form.get('username')
    user = User.get_or_none(User.username == username)
   
    if not user:
        flash("Username does not exist", "danger")
        return redirect(url_for('sessions.new'))
    
    check_password = check_password_hash(user.password, password)

    if not check_password:
        flash("Incorrect password", "warning")
        return redirect(url_for('sessions.new'))

    login_user(user)
    flash("logged in", "success")
    return redirect(url_for('index'))


@sessions_blueprint.route('/', methods=["GET"])
def index():
    return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("sessions.new"))


@sessions_blueprint.route('/new/google', methods=["GET"])
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google', methods=["GET"])
def authorize():
    token = oauth.google.authorize_access_token()
    email= oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

    user = User.get_or_none(User.email == email)

    if not user:
        flash('User not found, please sign up', 'danger')
        return redirect(url_for('new'))

    login_user(user)
    flash('Login successful', 'success')
    return redirect(url_for('index'))