from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template, request, flash
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/', methods=["GET"])
def new():
    return render_template("sessions/new.html")


@sessions_blueprint.route('/new', methods=['POST'])
def sign_in():
    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")
    # passw = User.get_or_none(User.password == login_password)

    user = User.get_or_none(User.email == login_email)
    # check in db if there is a user with the email we typed in in signin form

    checked = check_password_hash(user.password, login_password)

    if not user:  # CHANGE TO == USERID
        flash(f"Email does not exist")
        return redirect(url_for('sessions.new'))
    else:

        if not checked:
            flash(f"Password does not match our records")
            return redirect(url_for('sessions.new'))
        else:
            # session cannot store a whole python object, just the attritbute, so choose between id, name, email, etc
            # SESSION METHOD
            # session["user"] = user.id
            # session["name"] = user.name
            # FLASK METHOD
            login_user(user)
            flash(f"Login sucessful")
            # return redirect(url_for('sessions.new'))
            return redirect(url_for('home'))


@sessions_blueprint.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    flash(f"Logout sucessful")
    return redirect(url_for('sessions.new'))
