import peeweedbevolve
from flask import Blueprint, flash, Flask, render_template, request, flash, redirect, url_for, session
from models.user import User
from models.photos import Photos
from models.donation import Donation
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.s3_uploader import upload_file_to_s3
from operator import attrgetter
from PIL import Image, ImageOps
import tempfile

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/private', methods=['POST'])
def private():
    user = User.get_or_none(User.id == current_user.id)

    if not user:
        flash('No user id found')
        return redirect(url_for('users.show'))

    private = User.update(private_profile=True).where(
        User.id == current_user.id)

    private.execute()
    flash("successfully privated")
    return redirect(url_for('users.user_profile', id=current_user.id))


@users_blueprint.route('/unprivate', methods=['POST'])
def unprivate():
    user = User.get_or_none(User.id == current_user.id)

    if not user:
        flash('No user id found')
        return redirect(url_for('users.show'))

    unprivate = User.update(private_profile=False).where(
        User.id == current_user.id)
    unprivate.execute()

    flash("successfully UNprivated")
    return redirect(url_for('users.user_profile', id=current_user.id))


@users_blueprint.route('/new', methods=['GET'])
def new():
    user = User.get_or_none(User.id == id)
    users = User.get_or_none(User.id == id)
    return render_template('users/new.html', user=user, users=users)


@users_blueprint.route('/new/create', methods=['POST'])
def create():
    u_name = request.form.get("username")
    p_word = request.form.get("password")
    e_mail = request.form.get("email")

    c_user = User(name=u_name, password=p_word, email=e_mail)

    if c_user.save():
        flash("Sign Up success!")

        return redirect(url_for('users.new'))

    else:

        for error in c_user.errors:
            flash(error)
        return redirect(url_for('users.new'))


@users_blueprint.route('/upload', methods=["POST"])
@login_required
def upload():
    if not 'profile_image' in request.files:
        flash('No images has been provided', 'warning')
        return redirect(url_for('users.user_profile', id=current_user.id))

    file = request.files.get('profile_image')

    # new_img = Image.open(file)

    # new_img = ImageOps.fit(new_img, (500, 500), method=3,
    #                       bleed=0.0, centering=(0.5, 0.5))

    file.filename = secure_filename(file.filename)

    if not upload_file_to_s3(file):
        flash('Ops x loading!')
        return redirect(url_for('users.user_profile', id=current_user.id))
    user = User.get_or_none(User.id == current_user.id)
    user.profile_image = file.filename
    user.save()
    # newImage = User.get(User.id == current_user.id).profile_image
    # newImage = ImageOps.fit(file, (500, 500), method=3,
    #                         bleed=0.0, centering=(0.5, 0.5))
    # user.profile_image = newImage
    # user.save()

    flash('Upload success!', 'success')
    return redirect(url_for('users.user_profile', id=current_user.id))


@users_blueprint.route('/', methods=["GET"])
def index():

    return "USERS"


@users_blueprint.route('/profile/<id>', methods=['GET'])
@login_required
def user_profile(id):
    user_id = User.get_or_none(User.id == id)
    user = User.get_or_none(User.id == id)
    users = User.get_or_none(User.id == id)
    if not user_id:
        return redirect(url_for('home'))

    return render_template('users/userProfile.html', user_id=user_id, user=user, users=users)


@users_blueprint.route('/profile/<id>/update', methods=['POST'])
@login_required
def user_profile_update(id):
    user = User.get_or_none(User.id == id)
    if not current_user:
        flash('You unauthorized to do so!')
        return redirect(url_for('users.user_profile', id=id))

    else:
        if not user:
            flash("There doesn't seem to be a user with that id. Check again?")

            return redirect(url_for('users.user_profile', id=id))

        else:
            NewUser = request.form.get("NewUser")
            NewEmail = request.form.get("NewEmail")

            # user = user(name=NewUser, email=NewEmail)
            user.name = NewUser
            user.email = NewEmail

            user.save()
            flash("User details updated successfully!", 'success')

            return redirect(url_for('users.user_profile', id=id))


# @users_blueprint.route('/')
# def login_status():
#     if User.name in session:
#         return 'Logged in as %s' % escape(session[User.name])
#     return 'You are not logged in'


@users_blueprint.route('/login', methods=['POST'])
def login():
    # if request.method == 'POST':
    #     session[User.name] = request.form.get("logUser")
    #     return redirect(url_for('users.login_status'))
    # login = request.form.get("logUser")
    # sessions['logStatus'] = login
    # sessions.modified = True
    pass


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route("/newsfeed", methods=["GET"])
def show():

    images = []
    users = User.select()
    for user in users:
        last_image = Photos.select().where(Photos.user_id == user.id).order_by(
            Photos.created_at.desc()).limit(1)
        if len(last_image) > 0:
            images.append(last_image[0])

    images.sort(key=lambda image: image.created_at)
    images.reverse()

    # uz = User.get_or_none(User.id == id)

    return render_template('users/new.html', images=images)


@users_blueprint.route("/search", methods=["POST"])
def search_user():
    search_user = request.form.get("search_user")
    target_user = User.get_or_none(User.name == search_user)

    if not target_user:
        return redirect(url_for('users.show'))

    return redirect(url_for('users.user_profile', id=target_user.id))
