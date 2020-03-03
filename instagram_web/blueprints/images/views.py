from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
from models.user import User
from flask_login import current_user
from werkzeug.utils import secure_filename
from s3_uploader import upload_file_to_s3
from config import Config
from models.images import Image
from config import Config


images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/upload/image', methods=['POST'])
def upload_image():

    file = request.files.get('user_image')
    file.filename = secure_filename(file.filename)

    if file:
        if not upload_file_to_s3(file):
            flash('Something wrong', 'warning')
            return redirect(url_for('users.profile', id=current_user.id))

        user = User.get_or_none(User.id == current_user.id)
        image = Image(user_image=f'http://jynmunbucket.s3.amazonaws.com/' + file.filename,
                      user_id=user.id)

        # image.user_image = file.filename

        image.save()

    else:
        flash("file can't be uploaded", 'warning')
        return redirect(url_for('users.profile', id=current_user.id))

    flash('Successfully updated')
    return redirect(url_for('users.profile', id=current_user.id))
