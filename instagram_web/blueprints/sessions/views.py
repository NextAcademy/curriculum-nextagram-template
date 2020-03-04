import peeweedbevolve
from flask import Blueprint, flash, Flask, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user
from instagram_web.util.google_oauth import oauth


sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize/google")
def authorize():
    token = oauth.google.authorize_access_token()
    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        user = User.get_or_none(User.email == email)

        if not user:
            flash('No user registered with this account')
            return redirect(url_for(app.home))

        else:
            login_user(user)
            flash(f"Welcome Back {user.name}")
            return redirect(url_for("users.user_profile", id=current_user.id))

    #     login_user(user)
    #     return redirect('/somewhere')
    # else:
    #     return redirect('/somewhere')


@sessions_blueprint.route("/", methods=["GET"])
def new():
    return render_template("sessions/new.html")


@sessions_blueprint.route("/new", methods=["POST"])
def sign_in():
    # email = request.form.get("email")
    logUser = request.form.get("logUser")
    logPass = request.form.get("logPass")
    user = User.get_or_none(User.name == logUser)
    if not user:
        flash("Hmm. We can't seem to find you. Did you insert the correct user?")
        return render_template("sessions/new.html")
    hashed_password = user.password
    if not check_password_hash(hashed_password, logPass):
        flash("That password is incorrect. Please try again.")
        return render_template("sessions/new.html")
    login_user(user)
    flash(f"Welcome back {user.name}! You are now logged in")
    return redirect(url_for("sessions.new"))


@sessions_blueprint.route("/logout", methods=['POST'])
def logout():
    logout_user()
    flash("Successfully logged out. Goodbye!")
    return redirect(url_for("sessions.new"))


# @sessions_blueprint.route('/index')
# def new():

#     return render_template('sessions/new.html')


# @sessions_blueprint.route('/logout', methods=['POST'])
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     flash("Successfully logged out")
#     return redirect(url_for('sessions.index'))


# @sessions_blueprint.route('/index')
# def index():
#     if 'username' in session:
#         flash(f"Welcome Back {session['username']}!")
#         return render_template('sessions/new.html')
#     else:
#         flash('No User Logged In')
#         return render_template('sessions/new.html')


# @sessions_blueprint.route('/login/', methods=['POST'])
# def login():
#         # Check for the user in the db
#     logUser = request.form.get("logUser")
#     logPass = request.form.get("logPass")

#     user = User.get_or_none(User.name == logUser)

#     if user:
#         result = check_password_hash(user.password, logPass)

#         if result:

#             session['username'] = logUser
#             flash("Log in successful")
#             return redirect(url_for('sessions.index'))
#         else:
#             flash('Ooops!')
#             return redirect(url_for('users.new'))
#     else:
#         flash('something')
#         return redirect(url_for('home'))
