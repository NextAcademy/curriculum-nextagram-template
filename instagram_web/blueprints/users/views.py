from flask import Blueprint, flash, render_template,request,redirect,url_for,session,abort
from models.user import User
#---------------------DAY 2--------------------------------------------
from flask_login import login_user,login_required,logout_user,current_user
#-----------------------END------------------------------------------
#---------------------DAY 3--------------------------------------------
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET,S3_LOCATION
#-----------------------END------------------------------------------

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

#---------------------DAY 2--------------------------------------------
@users_blueprint.route('/login', methods=["GET"])
def login():
    return render_template('users/login.html')

@users_blueprint.route('/auth', methods=["POST"])
def authentication():
    # username=request.form['name'], password=request.form['password']
    username = request.form['name']
    password = request.form['password']

    try:
        user = User.get(name=username)
    except:
        flash('Username does not exist. Please try again.')
        return redirect(url_for('users.login'))

    login_user(user)
    flash('Logged in successfully.')
    return redirect(url_for('home'))

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))
#-------------------------END----------------------------------------


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user = User(
        name=request.form['name'],
        email=request.form['email'],
        password=request.form['password']
    )

    # ------------ this part is similar to authentication() function---------
    # to see if can implement DRY
    if user.save():
        flash("User created!")
        username = user.name
        try:
            user = User.get(name=username)
        except:
            flash('Username does not exist. Please try again.')
            return redirect(url_for('users.login'))

        login_user(user)
        flash('Logged in successfully.')
    #--------------------------- END-----------------------------------------------
        return redirect(url_for('home'))
    else:
        flash("Unable to create user!")
        return render_template('users/new.html', errors=user.errors) 


#---------------------DAY 2--------------------------------------------
@users_blueprint.route('/<username>', methods=["GET"])
def show(username): # user profile page
    try:
        user = User.get(name=username)
    except:
        abort(404)
    return render_template('users/profile_page.html',user=user,S3_LOCATION=S3_LOCATION)
#-------------------------END----------------------------------------


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

# ----------- DAY 3 -----------------------------------------------------------
@users_blueprint.route('/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    if current_user.id != id:
        abort(403)
    else:
        return render_template('users/edit_user.html',id=id)

# Method for changing email
@users_blueprint.route('/<int:id>/update_email', methods=['POST'])
@login_required
def update_email(id):
    if id != current_user.id:
        abort(403)

    form_email = request.form['new_email']
    form_password=request.form['password_1']
    user=User.get_by_id(id)

    # check password
    match = check_password_hash(user.password,form_password)
    if not match:
        flash("Incorrect password. Please try again")
        return redirect(url_for('users.edit',id=id))
    
    # check email
    email_exists=User.get_or_none(email=form_email)

    if email_exists:
        flash("This email is used by another account. Please try a different email.")
        return redirect(url_for('users.edit',id=id))
    else: 
        user = User(
            id=id,
            email=form_email
        )

        if user.save(only=[User.email]):
            # logout_user()
            # login_user(update_user)
            flash("Email updated!")
            return redirect(url_for('home'))
        else:
            flash("Unable to change email!")
            # asd
            return render_template('users/edit_user.html',id=id, errors=user.errors)

# Method for changing password
@users_blueprint.route('/<int:id>/update_password', methods=['POST'])
@login_required
def update_password(id):
    if id != current_user.id:
        abort(403)

    new_password_1 = request.form['new_password_1']
    new_password_2 = request.form['new_password_2']
    current_password = request.form['password_2']
    
    if new_password_1 != new_password_2:
        flash("New passwords do not match. Please try again.")
        return redirect(url_for('users.edit',id=id))

    user=User.get_by_id(id)

    # check password
    match = check_password_hash(user.password,current_password)
    if not match:
        flash("Incorrect password. Please try again")
        return redirect(url_for('users.edit',id=id))

    # update password
    user = User(
        id=id,
        password=new_password_1
    )

    if user.save(only=[User.password]):
        flash("Password updated!")
        return redirect(url_for('home'))
    else:
        flash("Unable to update password!")
        return render_template('users/edit_user.html',id=id, errors=user.errors)

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

# --------------- Day 3 Upload profile photo ----------------------------
@users_blueprint.route('/<int:id>/profile_photo', methods=["GET"])
@login_required
def profile_photo(id, image=""):
    return render_template('users/profile_photo.html',image=image)

@users_blueprint.route('/<int:id>/upload_profile_photo', methods=["POST"])
@login_required
def upload_file_to_s3(id):
    if id!=current_user.id:
        abort(403)

    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )

    file = request.files["profile_photo"]
    image_path= current_user.name + "/images/profile-pic/"+ file.filename

    s3.upload_fileobj(
        file,
        S3_BUCKET,
        image_path,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )
    file_loc = S3_LOCATION + image_path
    flash('Image uploaded successfully.')

    # save photo url in database
    user = User.get_by_id(id)
    user.profile_photo=image_path

    if user.save(only=[User.profile_photo]):
        flash("Profile photo saved to database successfully!")
    else:
        flash("Unable to save profile photo to database.")
    return render_template('users/profile_photo.html', image=file_loc,errors=user.errors)
# ----------------------- END -----------------------------------------
