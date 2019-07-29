import peewee
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user
from models.fan_idol import FanIdol
from models.user import User
from models.image import Image
from models.donation import Donation
from models.comment import Comment
from instagram_web.util.helpers import allowed_file, upload_file_to_s3


fan_idol_blueprint = Blueprint('fan_idol',
                            __name__,
                            template_folder='templates')

@fan_idol_blueprint.route('/follow/<id>', methods=['POST'])
def follow(id):
    user = User.get_by_id(id)
    if user.private:
        new = FanIdol(idol_id=id, fan_id=current_user.id)
        new.save()
        flash("Waiting for user approval", "info")
    else: 
        new = FanIdol(idol_id=id, fan_id=current_user.id, approved='true')
        new.save()
        flash("Thank you for following", "success")

    return redirect(url_for('users.show', username=user.username))
    

@fan_idol_blueprint.route('/unfollow/<id>', methods=['POST'])
def unfollow(id):
    user = User.get_by_id(id)
    unfollow_user = FanIdol.delete().where((FanIdol.fan_id == current_user.id) & (FanIdol.idol_id == user.id))
    unfollow_user.execute()


    flash(f"You are no longer following {user.username}", "danger")
    return redirect(url_for('users.show', username=user.username))

@fan_idol_blueprint.route('/approve/<id>', methods=['POST'])
def approve(id):
    update = FanIdol.update(approved='true').where((FanIdol.fan_id==id) & (FanIdol.idol_id == current_user.id))
    update.execute()
    return redirect(url_for('users.show', username=current_user.username))