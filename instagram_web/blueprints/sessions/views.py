from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import LoginManager, login_required, login_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/login', methods={'GET','POST'})
def login():
    # errors = None
    if request.method == 'POST':

        email = request.form.get('login_email')
        password = request.form.get('login_password')

        user_login = User.get(User.email==email)
        hashed_pw = user_login.password
        test_passwords = check_password_hash(hashed_pw, password)

        if test_passwords:
            login_user(user_login)
            flash(f"Hello {user_login.first_name}. You've signed in!")
            return redirect(url_for('home'))
        else:
            flash("Sign in unsuccessful. Please try again.")
            return render_template('sessions/login.html')

    return render_template('sessions/login.html')

@sessions_blueprint.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@sessions_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f"Goodbye.")
    return redirect(url_for('sessions.login'))