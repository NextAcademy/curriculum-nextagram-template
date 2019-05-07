from instagram_web.blueprints.images.helpers import upload_file_to_s3
import os
from app import app
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from models.user import User
from werkzeug import secure_filename


images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')


@images_blueprint.route('/', methods=["POST"])
def upload_file():

    if "user_file" not in request.files:
        flash('No user_file key in request.files')

    else:
        file = request.files["user_file"]

    if file.filename == "":
        flash('Please provide a file name')

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)
    else:
        return redirect('/')
