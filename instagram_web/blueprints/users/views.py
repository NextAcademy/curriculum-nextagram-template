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
#---------------------DAY 4--------------------------------------------
import peewee as pw
from models.image import Image
#-----------------------END------------------------------------------
from models.account_follower import Account_follower


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# Create new user
@users_blueprint.route('/', methods=['POST'])
def create(*args):

    try:
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password']
        )
    except:
        for item in args:
            print("In create new user, except route.")
            print(item)

    # ------------ this part is similar to authentication() function---------
    # to see if can implement DRY
    if user.save():
        flash("User created!")
        username = user.name
        try:
            user = User.get(name=username)
        except:
            flash('Username does not exist. Please try again.',"danger")
            return redirect(url_for('users.login'))

        login_user(user)
        flash('Logged in successfully.',"info")
    #--------------------------- END-----------------------------------------------
        return redirect(url_for('home'))
    else:
        flash("Unable to create user!","danger")
        return render_template('users/new.html', errors=user.errors) 

#---------------------DAY 2--------------------------------------------
# Shows user profile page
@users_blueprint.route('/<username>', methods=["GET"])
def show(username): 
    try:
        user = User.get(name=username)
    except:
        abort(404)
    
    
    image_list = pw.prefetch(Image.select().where(Image.user_id==user.id),User)
    followers = User.select().where(User.id==user.id).join(Account_follower,on=(User.id==Account_follower.account_id))

    for follower in followers: #<----- NEXT TO CHECK
        print("Followers: ") 
        print(follower.name)

    return render_template('users/profile_page.html',user=user,S3_LOCATION=S3_LOCATION,image_list=image_list)
#-------------------------END----------------------------------------

# Indexes all users
@users_blueprint.route('/', methods=["GET"])
def index():
    users=User.select()
    return render_template('users/users.html',users=users,S3_LOCATION=S3_LOCATION)

# ----------- DAY 3 -----------------------------------------------------------
# Edit user settings page
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
        flash("Incorrect password. Please try again","danger")
        return redirect(url_for('users.edit',id=id))
    
    # check email
    email_exists=User.get_or_none(email=form_email)

    if email_exists:
        flash("This email is used by another account. Please try a different email.","danger")
        return redirect(url_for('users.edit',id=id))
    else: 
        user = User(
            id=id,
            email=form_email
        )

        if user.save(only=[User.email]):
            # logout_user()
            # login_user(update_user)
            flash("Email updated!","info")
            return redirect(url_for('home'))
        else:
            flash("Unable to change email!","danger")
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
        flash("New passwords do not match. Please try again.","danger")
        return redirect(url_for('users.edit',id=id))

    user=User.get_by_id(id)

    # check password
    match = check_password_hash(user.password,current_password)
    if not match:
        flash("Incorrect password. Please try again","danger")
        return redirect(url_for('users.edit',id=id))

    # update password
    user = User(
        id=id,
        password=new_password_1
    )

    if user.save(only=[User.password]):
        flash("Password updated!","info")
        return redirect(url_for('home'))
    else:
        flash("Unable to update password!",'danger')
        return render_template('users/edit_user.html',id=id, errors=user.errors)

# Method for changing privacy settings
@users_blueprint.route('/<int:id>/privacy', methods=['POST'])
@login_required
def toggle_privacy(id):
    if id != current_user.id:
        abort(403)
    user=User.get_by_id(id)
    user.private= not user.private

    if user.save():
        flash("Privacy settings updated successfuly.")
    else:
        flash("Privacy settings could not be changed!")
    return redirect(url_for('users.edit',id=id))

# --------------- Day 3 Upload profile photo ----------------------------
# Upload profile photo page
@users_blueprint.route('/<int:id>/profile_photo', methods=["GET"])
@login_required
def profile_photo(id, image=""):
    return render_template('users/profile_photo.html',image=image)

# Uploads file to Amazon S3
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
    flash('Image uploaded successfully.','info')

    # save photo url in database
    user = User.get_by_id(id)
    user.profile_photo=image_path

    if user.save(only=[User.profile_photo]):
        flash("Profile photo saved to database successfully!",'info')
    else:
        flash("Unable to save profile photo to database.",'danger')
    return render_template('users/profile_photo.html', image=file_loc,errors=user.errors)
# ----------------------- END -----------------------------------------

