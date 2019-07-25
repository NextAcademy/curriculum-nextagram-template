from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from flask_login import login_user

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates/sessions')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.email == request.form.get('email'))

    if not user:
        flash(
            f"No account registered under the email {request.form.get('email')}", 'warning')
        return redirect(url_for('sessions.new'))

    login_user(user)

    flash(f'Welcome back, {user.username}', 'success')
    return redirect(url_for('users.index'))
