from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.user import User
from models.user_images import Image
from flask_login import current_user
from helpers import upload_file_to_s3
from config import S3_BUCKET, S3_LOCATION
from werkzeug.utils import secure_filename

images_blueprint = Blueprint('images', __name__, template_folder='templates')


@images_blueprint.route('/new/<id>', methods=['GET'])
def new(id):
    if int(id) == current_user.id:
        return render_template('/new.html')

    else:
        flash(
            f'Sorry but you do not have access to that.', 'danger')
        return redirect(request.referrer)


@images_blueprint.route('/create/<id>', methods=['POST'])
def create(id):
    if "user_file" not in request.files:
        flash("No file was chosen! :O", 'warning')
        return redirect(url_for('users.show', username=current_user.username))
    file = request.files.get('user_file')
    file_name = secure_filename(file.filename)
    if file_name != '':
        caption = request.form.get('caption')
        error = str(upload_file_to_s3(file, S3_BUCKET))
        new_image = Image(
            source=S3_LOCATION + file_name, user_id=current_user.id, caption=caption)

        if new_image.save():
            return redirect(url_for('users.show', username=current_user.username))
        else:
            return render_template('users/profile.html', error=error)
    else:
        flash('File has no name!', 'warning')
        return redirect(url_for('users.show', username=current_user.username))
