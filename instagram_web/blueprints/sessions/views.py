from flask import Blueprint, render_template, request, redirect, url_for, flash, session, escape
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models.user import User
from app import login_manager
from flask_login import login_user, login_required, logout_user
from helpers import oauth  




sessions_blueprint = Blueprint('sessions', #this blueprint is called sessions
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# @sessions_blueprint.route('/')
# def index():
  
#     return render_template('sessions/user_signin.html')
    

@sessions_blueprint.route('/login', methods=['POST'])
def login():
    password_to_check = request.form['password']
    name = request.form.get('name')
    user = User.get(User.name == name)
    
    result = check_password_hash(user.password, password_to_check)

    if  result:    
       
        login_user(user)

        flash('Logged in successfully.')

        return redirect(url_for('users.show', name=user.name))
       
    flash("Sign in failed")
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return "logged out"

@sessions_blueprint.route("/google", methods=['GET'])
def google_authorize():
    redirect_uri = url_for('sessions.google_sign_in', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)




@sessions_blueprint.route("/authorize/google", methods=['GET'])
def google_sign_in():
     token = oauth.google.authorize_access_token()
     email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

     user = User.get(User.email == email)

     login_user(user)

     flash('Logged in successfully.')

     return redirect(url_for('users.show', name=user.name))








