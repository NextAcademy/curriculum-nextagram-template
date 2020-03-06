from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required
from flask_login import current_user
from models.images import Image
from models.donations import Donation
from instagram_web.util.braintree import gateway
import requests
from config import Config
from models.user import User
from models.follower_following import FollowerFollowing

follower_following_blueprint = Blueprint('follower_following',
                                         __name__,
                                         template_folder='template')


@follower_following_blueprint.route('/<idol_id>', methods=["GET", "POST"])
@login_required
def create(idol_id):
    idol = User.get_or_none(User.id == idol_id)
    follow = FollowerFollowing(fan_id=current_user.id, idol_id=idol.id)
    if follow.save():
        flash(f"Following {idol.username} successful")
        return redirect(url_for('users.profile', id=idol.id))

    else:
        flash("Follow unsuccessful, guess you shouldn't after all")
        return redirect(url_for('home'))


@follower_following_blueprint.route('/<idol_id>/delete', methods=["GET", "POST"])
@login_required
def delete(idol_id):
    idol = User.get_or_none(User.id == idol_id)
    unfollow = FollowerFollowing.get_or_none(
        fan_id=current_user.id, idol_id=idol.id)
    if unfollow.delete_instance():
        flash(f"Unfollowed {idol.username}")
        return redirect(url_for('home'))

    else:
        flash("Unfollow unsuccessful, guess you're forced to be a good person")
        return redirect(url_for('users.profile', id=idol.id))


@follower_following_blueprint.route('/<fan_id>/accept', methods=["GET", "POST"])
@login_required
def accept(fan_id):
    fan = User.get_or_none(User.id == fan_id)
    follow = FollowerFollowing(idol_id=current_user.id, fan_id=fan.id)
    if follow.save():
        flash(f"Accepted {fan.username}. They can now see all your posts.")
        return redirect(url_for('users.profile', id=fan.id))

    else:
        flash("Unsuccessful, guess they're too creepy to accept.")
        return redirect(url_for('home'))
