from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/sign_in', methods=['POST'])
def sign_in():
    username = request.form.get('username')
    password = request.form.get('password')
    if User.get_or_none(User.username == username):
        user = User.get(User.username == username)
        hashed_pass = user.password
        if check_password_hash(hashed_pass, password):
            session['user_id'] = user.id
            flash('ye, you is in')
            return redirect(url_for('users.index'))
        else:
            flash('right name, wrong pass')
            return render_template('sessions/new.html')
    else:
        flash("bruh, you don't exist")
        return render_template('sessions/new.html')
