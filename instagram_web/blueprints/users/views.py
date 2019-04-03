from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from werkzeug.security import generate_password_hash
from  flask_login import current_user
from helpers import s3
from peewee import prefetch


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    s = User(name=request.form['name'], email=request.form['email'], password= generate_password_hash(request.form['password']))

    if s.save():
        flash("Successfully saved")
        return redirect(url_for("sessions.new"))
    else:
        return render_template('users/new.html', errors=s.errors)
    


@users_blueprint.route('/<name>', methods=["GET"])
def show(name):
    return render_template('users/user_page.html')


@users_blueprint.route('/', methods=["GET"])
def index():

    users= User.select()
    user_images= Image.select()
    user_with_images= prefetch(users, user_images)
    return render_template('home.html', users=user_with_images)


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit_page.html',id=id)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    name = request.form['name']
    email = request.form['email']
    old_password = request.form['old_password']
    confirm_password = request.form['confirm_password']
    password = request.form['password']       

    if current_user == user and old_password == confirm_password:
        s=(User.update({User.name: name, User.email:email, User.password: generate_password_hash(password)}).where(User.id == id))
        s.execute()
        return redirect (url_for('users.show', name=user.name))
    else:
        return "nothing"
   
@users_blueprint.route('/<id>/profile_pic/edit', methods=['GET'])
def profile_pic_edit(id):
    return render_template('users/profilepic_edit_page.html', id = id)

@users_blueprint.route('/<id>/profile_pic/update', methods=['POST'])
def profile_pic_update(id):

    file=request.files.get("user_file")
    s=(User.update({User.profile_picture: file.filename}).where(User.id==id))
    s.execute()
    s3.upload_fileobj(
        file,
        "nextagramtao",
        file.filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )
    return redirect(url_for('users.show', name= current_user.name))

@users_blueprint.route('/<id>/upload_image/edit', methods=['GET'])
def upload_image(id):
    return render_template('users/upload_image.html', id=id)

@users_blueprint.route('<id>/upload_image/update', methods=['POST'])
def upload_image_update(id):
    file=request.files.get("user_file")
    s = Image(user=id,image_url=file.filename)
    s.save()
    s3.upload_fileobj(
        file,
        "nextagramtao",
        file.filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )
    return redirect(url_for('users.show', name=current_user.name))
    
