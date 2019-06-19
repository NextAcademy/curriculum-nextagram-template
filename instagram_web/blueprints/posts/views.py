from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from models.post import Post
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user
from instagram_web.util.helpers import upload_file_to_s3
from app import app

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates')

@posts_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('posts/new.html')

@posts_blueprint.route('/', methods=['POST'])
def create():
    if "newpic" not in request.files:
        return "No newpic key in request.files"

    file = request.files["newpic"]

    if file.filename == "":
        return "Please select a file"

	# D.
    if file and current_user.is_authenticated:
    # if file and allowed_file(file.filename):
        # file.filename = secure_filename(file.filename)
        filename = file.filename
        # output = upload_file_to_s3(file, app.config["S3_BUCKET"], filename=str(current_user.id)+'/'+filename)
        upload_file_to_s3(file, app.config["S3_BUCKET"], filename=str(current_user.id)+'/'+filename)
        new_post = Post(user_id = current_user.id, post_image = filename)
        new_post.save()
        return redirect(url_for('users.show', username=current_user.username))
        #http://my-bucket-now.s3.amazonaws.com/Screenshot_168.png

    else:
        return redirect("/")
