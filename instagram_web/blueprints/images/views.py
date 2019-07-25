from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image

images_blueprint = Blueprint(
    'images', __name__, template_folder='templates'
)


@images_blueprint.route('/upload/profile', methods=['POST'])
@login_required
def create_profile():
    file = request.files['image_file']

    if not file:
        flash('No file provided', 'warning')
        return redirect(url_for('users.edit', id=current_user.id))

    file.filename = secure_filename(file.filename)

    output = upload_file_to_s3(file)

    if not output:
        flash('Error uploading image', 'warning')
        return redirect(url_for('users.edit', id=current_user.id))

    user = User.get_or_none(User.id == current_user.id)

    user.profile_picture = output

    user.save()

    flash('Successfully updated profile picture', 'success')
    return redirect(url_for('users.edit', id=current_user.id))


@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')


@images_blueprint.route('/upload', methods=['POST'])
@login_required
def create_image():
    file = request.files['image_file']
    caption = request.form.get('caption')

    if not file:
        flash('No file provided', 'warning')
        return redirect(url_for('images.new'))

    file.filename = secure_filename(file.filename)

    output = upload_file_to_s3(file)

    if not output:
        flash('Error uploading image', 'warning')
        return redirect(url_for('images.new'))

    image = Image(
        user_id=current_user.id,
        caption=caption,
        image_name=file.filename
    )

    if not image.save():
        flash('Error creating post', 'warning')
        return redirect(url_for('images.new'))

    flash('Successfully created new post', 'success')
    return redirect(url_for('users.index'))
