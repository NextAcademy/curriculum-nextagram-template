from flask import Flask, Blueprint, request, redirect, url_for, render_template, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/signin', methods=["GET"])
def show():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=["POST"])
def sign_in():
    email = request.form.get('email')
    password_to_check = request.form.get('password')

    user = User.get_or_none(User.email == email)

    if not user:
        flash(f"{email} is incorrect.")
        return render_template('sessions/new.html')

    hashed_password = user.password

    if not check_password_hash(hashed_password, password_to_check):
        flash("Incorrect password! Please try again!")
        return render_template('sessions/new.html')

    session['user_id'] = user.id
    flash(f"Welcome back {user.username}. You are logged in!")
    return redirect(url_for('home'))


# @sessions_blueprint.route('/login', methods=["POST", "GET"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         login_user(user)
#         flash('Logged in successfully.')
#         next = flask.request.args.get('next')
#         if not is_safe_url(next):
#             return flask.abort(400)

#         return redirext(next or url_for('index'))
#     return render_template('sessions/new.html', form=form)

#     { % if current_user.is_authenticated % }
#     Hi {{current_user.name}}!
#     { % endif % }


# @sessions_blueprint.route("/settings")
# @login_required
# def settings():
#     pass


# @sessions_blueprint.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect url_for('sessions/new')
