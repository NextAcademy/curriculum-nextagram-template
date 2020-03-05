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

    if user.is_followed:
        flash('you are already following that user', 'error')

    new_follow = Follow(fan_id=current_user.id, idol_id=id)
    if not new_follow.save():
        flash('sorry, could not process the request:(', 'danger')
        return redirect(request.referrer)

    flash('Followed successfully!!', 'success')
    return redirect(request.referrer)
