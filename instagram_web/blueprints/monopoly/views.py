from flask import Blueprint, render_template, request, flash,  redirect, url_for
from models.mon_user import Mon_User
from flask_login import current_user, login_user, login_required
from models.user import User


monopoly_blueprint = Blueprint(
    'monopoly', __name__, template_folder='templates')


@monopoly_blueprint.route('/')
def index():
    if current_user.is_authenticated:
        users = User.select().where(User.monopoly > 0)
        user_positions = []
        for user in users:
            user_positions.append(user.position)
        return render_template('monopoly/index1.html', user_positions=user_positions)

    else:
        flash('login is required', 'danger')
        return redirect(request.referrer)


# @monopoly_blueprint.route('/new')
# def new():
#     return render_template('users/new.html')


@monopoly_blueprint.route('/create')
def create():
    user = User.get_or_none(User.id == current_user.id)
    if user.monopoly > 0:
        user.monopoly = 0
    else:
        user.monopoly = 1

    if user.save():
        flash('updated successfully', 'success')

    else:
        flash('failwhale', 'danger')

    return redirect(request.referrer)
