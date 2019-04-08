from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models.image import Image
from flask_login import current_user
from instagram_web.helpers.helpers import upload_file_to_s3, allowed_file
from werkzeug.utils import secure_filename
from app import app
import datetime


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/upload', methods=['GET'])
def new():
    return render_template('images/uploadpic.html')

@images_blueprint.route('/images/<id>/upload', methods=['POST'])
def create(id):
    id = current_user.id
    caption = request.form.get('caption')
    user_id = current_user.id

    if "user_file" not in request.files:
        flash("Please select a file to upload", "danger")

    file = request.files["user_file"]

    if file.filename == "":
        flash("Please choose a file that has a name", "danger")
    
    if file and allowed_file(file.filename):
        file.filename = secure_filename(str(id) + "_" + file.filename + str(datetime.datetime.now()))
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        image = Image(caption=caption, user_id=user_id, image_path=output)
        if image.save():
            flash("Successfully uploaded image", "success")
            return redirect(url_for('images.new', id=current_user.id))
        else:
            flash("Failed to upload image", "danger")
            return redirect(url_for('images.new', id=current_user.id))

    else:
        return redirect(url_for('users.profile'))
