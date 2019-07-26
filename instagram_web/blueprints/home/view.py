from app import app
from flask import render_template, request, url_for,redirect, flash
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import current_user
from models.user import Images, Follows
from jinja2 import Template

home_blueprint = Blueprint('home',
                            __name__,
                            template_folder='templates')

@home_blueprint.route("/", methods=["GET"])
def index():

    if(current_user.is_authenticated):
        feed_images = Images.select().where(Images.user.in_(current_user.following())).order_by(Images.created_at.desc())
        myidols = User.select().join(Follows, on=(Follows.myidol_id == User.id)).where(Follows.myfan_id == current_user.id)
        return render_template('home.html', feed_images = feed_images, user=myidols)
    else:
        return render_template('signin.html')
