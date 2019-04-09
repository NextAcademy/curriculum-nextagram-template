from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.helpers.google_oauth import oauth


import config
import os


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')
    

@sessions_blueprint.route('/login', methods=["POST"])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get(User.username == username)
    if not user:
        # Flash a message
        flash("Username or password is incorrect", "danger")
        return redirect(url_for('sessions.new'))
    else:
        if check_password_hash(user.password, password):
            login_user(user)
            flash("Successfully logged in.", "success")
            return redirect(url_for('users.show', id=current_user.id))
        else:
            flash("Username or password is incorrect", "danger")
            return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/oauth', methods=["POST"])
def g_new():
    redirect_url = url_for('sessions.g_login', _external = True )
    return oauth.google.authorize_redirect(redirect_url)

@sessions_blueprint.route('/authorize/google', methods=["GET"])
def g_login():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        flash("You have logged in", "success")
        login_user(user)
        return redirect(url_for('users.show', id = user.id ))
    else:
        flash('You are not NOT logged in', "danger")
        return redirect(url_for('sessions.new'))
