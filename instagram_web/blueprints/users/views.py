from flask import Blueprint, flash, render_template,request,redirect,url_for,session,abort
from models.user import User
#---------------------DAY 2--------------------------------------------
from flask_login import login_user,login_required,logout_user,current_user
#-----------------------END------------------------------------------
#---------------------DAY 3--------------------------------------------
from werkzeug.security import check_password_hash
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


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


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
def update_email(id):
    form_email = request.form['new_email']
    form_password=request.form['password_1']
    user = User.get_by_id(id)

    # check if password matches user
    match = check_password_hash(user.password,form_password)
    if not match:
        flash("Incorrect password. Please try again")
        return redirect(url_for('users.edit',id=user.id))
    
    # check if email fulfills unique requirement
    email_check=User.get_or_none(email=form_email)

    if email_check: # email is used
        flash("This email is used. Please try a different email.")
        return redirect(url_for('users.edit',id=user.id))

    else: # create new user
        new_user = User(name=user.name, password=form_password, email=form_email)
        flash("Email updated!")
        return redirect(url_for('users.edit',id=new_user.id))



# ----------- END -------------------------------------------------------------


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
