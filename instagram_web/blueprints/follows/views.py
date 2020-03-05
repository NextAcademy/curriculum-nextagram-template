from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user
from models.follow import Follow
from models.user import User

follows_blueprint = Blueprint('follows', __name__, template_folder='templates')


@follows_blueprint.route('/<id>/create')
def create(id):
    if id == current_user.id:
        flash('you cannot follow yourself -.-', 'error')
        return redirect(request.referrer)

    user = User.get_or_none(User.id == id)
    if not user:
        flash('that user does not exist :(', 'danger')
        return redirect(request.referrer)

    if user.is_followed:
        flash('you are already following that user', 'danger')
        return redirect(request.referrer)

    new_follow = Follow(fan_id=current_user.id, idol_id=id)
    if not new_follow.save():
        flash('sorry, could not process the request:(', 'danger')
        return redirect(request.referrer)

    flash('Followed successfully!!', 'success')
    return redirect(request.referrer)


@follows_blueprint.route('/<id>/delete')
def delete(id):
    user = User.get_or_none(User.id == id)

    if not user:
        flash('sorry that user does not exist.')
        return redirect(url_for('users.index'))

    if not user.is_followed:
        flash('sorry, you are not currently following that user, so no need to unfollow.')
        return redirect(url_for('users.index'))

    follow = Follow.get_or_none(
        Follow.fan_id == current_user.id, Follow.idol_id == id)

    if not follow.delete_instance(recursive=True):
        flash(
            f'database shows no instance of you following {user.username}', 'danger')
        return redirect(request.referrer)

    flash('Unfollowed successfully', 'success')
    return redirect(request.referrer)


@follows_blueprint.route('/<id>/show/following')
def show_idols(id):

    idols = [user.idol for user in Follow.select().where(
        Follow.fan_id == current_user.id)]
    return render_template('follows/idols.html', idols=idols)


@follows_blueprint.route('/<id>/show/followers')
def show_fans(id):
    fans = [user.fan for user in Follow.select().where(
        Follow.idol_id == current_user.id)]
    return render_template('follows/fans.html', fans=fans)
