from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user import User


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/login', methods=["GET"])
def login_create():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/login', methods=["POST"])
def login_post():
    user_for_auth = User.get_or_none(User.email==request.form.get('email')) # captures User.id of the username if it exists
    if user_for_auth:
        password_to_check = request.form['password']
        hashed_password = user_for_auth.password
        result = check_password_hash(hashed_password, password_to_check) # this function return True or False to result
        if result:
            # let flask-login to take over
            # login_user(user_for_auth)
            session["user_id"] = user_for_auth.id
            flash('You are now logged in', 'success')
            return redirect('/')
        else:
            flash('Password is incorrect', 'danger')
    else:
        flash('That email address has not been registered', 'danger')

    return render_template('sessions/login.html', email=request.form['email'])
