import peeweedbevolve
from flask import Blueprint, flash, Flask, render_template, request, flash, redirect, url_for, session
from models.user import User
from models.photos import Photos
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.s3_uploader import upload_file_to_s3


imgs_blueprint = Blueprint('imgs',
                           __name__,
                           template_folder='templates')


@imgs_blueprint.route("/", methods=["POST"])
def create():
    if not 'image' in request.files:
        flash('No images has been provided', 'warning')
        return redirect(request.referrer)

    file = request.files.get('image')
    file.filename = secure_filename(file.filename)
    caption = request.form.get("caption")

    if not upload_file_to_s3(file):
        flash('Ops x loading!')
        return redirect(request.referrer)

    image = Photos(filename=file.filename, caption=caption,
                   user=current_user.id)

    if not image.save():
        flash('Didnt managed to upload')
        return redirect(request.referrer)

    flash('Upload success!', 'success')
    return redirect(request.referrer)
