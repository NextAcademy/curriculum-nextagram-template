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



# --------------- WORKING SECTION for update email ----------------------------
# -------------- creates new user after each change :( ------------------------
        # # create new acc w old name, old password, new email.
        # # old_pw = user.password
        # # old_name = user.name

        # new_user = User.create(
        #     name=user.name, 
        #     password=user.password, 
        #     email=form_email
        #     )
        
        # # asas
        # flash("Email updated!")
        # # 2. Logout current acc
        # logout_user() # to check if working

        # # 3. Delete old account code here
        # user.delete_instance()

        # # 4. login new acc
        # if new_user.save():
        #     login_user(new_user)
        #     return redirect(url_for('home'))
        # else:
        #     flash("Unable to create user!")
        #     return render_template('users/new.html', errors=user.errors) 

# ----------- END -------------------------------------------------------------


