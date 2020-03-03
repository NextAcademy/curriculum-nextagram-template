from flask import Flask, redirect, url_for, escape, request, Blueprint, render_template, request, flash
from models.userimages import UserImage
from flask_login import login_required, current_user

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=["GET"])
@login_required
def new(image_id):
    image = UserImage.get_or_none(UserImage.id == image_id)

    if not image:
        flash(f"No Image was found with the provided ID")
        return redirect(url_for('users.index'))

    return render_template('donations/new.html', image=image)
