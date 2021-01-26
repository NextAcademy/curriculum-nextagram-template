from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    # get data from the form
    username = request.form.get("username")
    password = request.form.get("password")

    # check if user exists in database
    user = User.get_or_none(User.username == username)

    if user:
        result = check_password_hash(user.password_hash, password)
        # if passwords match
        if result: 
            flash("Passwords matched", 'info')
            # save user id in browser session
            login_user(user)
            return redirect(url_for('users.show', username=user.username)) 
        else:  
            flash("Passwords not matched")
            return render_template("sessions/new.html")
    else: 
        flash("User not found")
        return render_template("sessions/new.html")

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    flash("Logout successful", 'info')
    return redirect(url_for("sessions.new"))

@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

# --- GOOGLE OAUTH STUFFS ---
@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Sign in successful", "success")
        return redirect(url_for('users.show', username=user.username))
    else:
        flash("Sign up to continue", "danger")
        return redirect(url_for('users.new'))