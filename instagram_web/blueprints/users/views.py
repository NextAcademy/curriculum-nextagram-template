from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from flask_login import login_required, login_user, current_user
from werkzeug import secure_filename
from instagram_web.util.helpers import upload_file_to_s3
import peewee as pw
from models.image import Image
from models.donation import Donation
import requests


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    params = request.form

    new_user = User(username=params.get("username"), email=params.get("email"), password=params.get("password"))

    if new_user.save():
        flash("Successfully signed up", 'success')
        # login new user after sign up
        login_user(new_user)
        # redirect users to Profile Page 
        return redirect(url_for('users.show', username=new_user.username))
    else:
        flash(new_user.errors)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.select().where(User.username == username).limit(1)
    if user:  
        user = pw.prefetch(user, Image, Donation)[0]
        return render_template("users/show.html", user=user)
    else:
        flash("No user found")
        return redirect(url_for("home")) 


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            return render_template("users/edit.html", user=user)
        else:
            flash("Cannot edit someone else's profile")
            return redirect(url_for('users.show', username=username))
    else:
        flash("No user found")
        return redirect(url_for("home"))


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    if user: 
        if current_user.id == int(id):
            params = request.form

            user.is_private = True if params.get("private") == "on" else False

            user.username = params.get("username")
            user.email = params.get("email") 
            # print("user.email")
            password = params.get("password")

            if len(password) > 0:
                user.password = password
                
            if user.save():
                flash("Successfully updated details")
                return redirect(url_for("users.show", username=user.username))
            else: 
                flash("Failed to edit the details. Try again.")
                return redirect(url_for("users.edit", id=user.id))
        
        else:
            flash("You cannot edit details of another user")
            return redirect(url_for("home"))
    else:
        flash("No such user found")
        return redirect(url_for("home"))

@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    user = User.get_or_none(User.id == id) 
    if user:
            if current_user.id == int(id):
                # upload the image
                if "profile_image" not in request.files:
                    flash("No file selected")
                    return redirect(url_for("users.edit", id=id))
                file = request.files["profile_image"]

                file.filename = secure_filename(file.filename)
            
                image_path = upload_file_to_s3(file, user.username)

                user.image_path = image_path

                if user.save():
                    return redirect(url_for("users.show", username=user.username))
                else:
                    flash("Upload failed, try again!")
                    return redirect(url_for("user.edit", id=id))
            else:
                flash("You cannot edit other profiles")
                return redirect(url_for("users.show", username=user.username))
    else:
        flash("No such user found")
        return redirect(url_for("home"))

@users_blueprint.route('<idol_id>/follow', methods = ['POST'])
@login_required
def follow(idol_id):
    idol = User.get_by_id(idol_id)

    if current_user.follow(idol):
        if current_user.follow_status(idol).is_approved:
            flash(f"You are now following {idol.username}", "info")
        else:
            flash(f"Your follow request has been sent to {idol.username}","info")
        return redirect(url_for('users.show'))
    else:
        flash("Unable to follow this user, try again.", "danger")
        return render_template(url_for('users.show', username=idol.username))

@users_blueprint.route('<idol_id>/unfollow', methods = ['POST'])
@login_required
def unfollow(idol_id):
    idol = User.get_by_id(idol_id)

    if current_user.unfollow(idol): 
        flash(f"You no longer follow {idol.username}",)