from flask import Blueprint, render_template, request, redirect, url_for, flash, session, escape
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models.user import User


sessions_blueprint = Blueprint('sessions', #this blueprint is called sessions
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/')
def index():
    if 'user_id' in session:
        return render_template('sessions/user_signin.html',user_id= (session['user_id']))
    return "you are not logged in"


@sessions_blueprint.route('/login', methods=['POST'])
def login():
    password_to_check = request.form['password']

    query= User.select()

    for user in query:

        result = check_password_hash(user.password, password_to_check)

        if  request.form['name'] == user.name and result:
            session["user_id"] = user.id
            flash("Sign in successfully")
            return redirect(url_for('sessions.index'))
       
    flash("Sign in failed")
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/logout', methods=['POST'])
def logout():
     session.pop('user_id', None)
     return redirect(url_for('sessions.index'))