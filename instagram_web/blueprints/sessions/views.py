from models.user import User
from instagram_web.util.google_oauth import oauth
from flask_login import login_user, login_required,logout_user
from flask import Blueprint,url_for,render_template, flash, redirect, request

# ----------------------------------------------------------------------------------------
sessions_blueprint=Blueprint('sessions',
                            __name__,
                            template_folder='templates')
# ----------------------------------------------------------------------------------------

@sessions_blueprint.route('/login', methods=["GET"])
def login():
    return render_template('sessions/login.html')

@sessions_blueprint.route('/auth', methods=["POST"])
def authentication():
    username = request.form['name']
    password = request.form['password']

    try:
        user = User.get(name=username)
    except:
        flash('Username does not exist. Please try again.')
        return redirect(url_for('sessions.login'))

    login_user(user)
    flash('Logged in successfully.')
    return redirect(url_for('home'))

@sessions_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

# ----------------------------------------------------------------------------------------
@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize',_external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    print("IN SESSIONS AUTHORIZE()")
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    profile_photo = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email==email)

    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        flash("User email not found in database. Please create an account first.")
        return redirect(url_for('users.new'))