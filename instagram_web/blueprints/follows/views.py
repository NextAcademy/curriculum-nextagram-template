import peeweedbevolve
from flask import Blueprint, flash, Flask, render_template, request, flash, redirect, url_for, session
from models.user import User
from models.photos import Photos
from models.donation import Donation
from models.FF import FF
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.s3_uploader import upload_file_to_s3
from instagram_web.util.braintree import gateway
from instagram_web.util.mailgun import send_simple_message


follows_blueprint = Blueprint('follows',
                              __name__,
                              template_folder='templates')


@follows_blueprint.route("/<idol_id>", methods=["POST"])
def create(idol_id):

    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash('No user with this id')
        return redirect(url_for('users.show'))

    new_follow = FF(fan_id=current_user.id, idol_id=idol_id)

    if not new_follow.save():
        flash('Unable to follow this person')
        return redirect(url_for('users.user_profile', id=idol_id))

    else:
        flash(f'You are now following {idol.name}')
        return redirect(request.referrer)


@follows_blueprint.route("/<idol_id>/delete", methods=["POST"])
def delete(idol_id):

    follow = FF.get_or_none((FF.idol_id == idol_id)
                            & (FF.fan_id == current_user.id))

    # follow.delete_instance(User.id == idol_id)

    if follow.delete_instance():
        flash(f'You have unfollowed {follow.idol.name}')
        return redirect(url_for('users.show'))
