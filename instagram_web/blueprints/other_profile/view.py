from app import app
from flask import render_template, request, url_for,redirect, flash
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, Follows
from flask_login import LoginManager,  login_user, current_user, logout_user

otherprofile_blueprint = Blueprint('others_profile',
                            __name__,
                            template_folder='templates')


@otherprofile_blueprint.route("/", methods=["POST","GET"])
def kkk():
    if(current_user.is_authenticated):
        # breakpoint()
        username = request.form.get('username')
        user = User.get_or_none(User.username == username)
        return render_template("others_profile.html", user=user)
    else:
        return render_template("signin.html")
    
    
@app.route("/<username>", methods=["POST", "GET"])
def follow(username):
  
    x = User.get_or_none(User.username == username)
    my_idols = User.select().join(Follows, on=(User.id == Follows.myidol_id)).where(Follows.myfan_id == current_user.id)

    follow = Follows(myfan_id = current_user.id, myidol_id= x.id)
    follow.save()
    # return redirect(url_for('others_profile.kkk', user=x))
    return render_template("others_profile.html", user=x, follows=my_idols)