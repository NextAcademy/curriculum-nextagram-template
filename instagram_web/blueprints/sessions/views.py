from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.user import User

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/login', methods={'GET','POST'})
def login():
    # errors = None
    if request.method == 'POST':
        email = request.form.get('login_email')
        password = request.form.get('login_password')

        hashed_pw = User.get(User.email==email).password
        test_passwords = check_password_hash(hashed_pw, password)

        if test_passwords:
            flash("Sign in successful")
            return redirect(url_for('home'))
        else:
            flash("Sign in unsuccessful. Try again.")
            return render_template('sessions/login.html')
        # get the email & password from db = if they match then redirect to home page
        # if no match, return error
    return render_template('sessions/login.html')
