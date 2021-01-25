from models.user import User
from models.account_follower import Account_follower
from flask import Blueprint, flash, render_template,request,redirect,url_for,session,abort
from flask_login import login_user,login_required,logout_user,current_user

followers_blueprint=Blueprint('followers',
                            __name__,
                            template_folder='templates')

# Send follow request
@followers_blueprint.route('/<int:acc_id>/<int:follower_id>', methods=["POST"])
@login_required
def create(acc_id,follower_id):
    new_follow=Account_follower(
        account = acc_id,
        follower=follower_id
    )
    username = User.get_by_id(acc_id).name
    user=User.get_by_id(acc_id)

    if new_follow.save():
        flash("Follow request sent!")
        return redirect(url_for('users.show',username=username))
    else:
        flash("Trouble sending follow request.")
        return render_template('home.html', errors=new_follow.errors)

# View follow requests
@followers_blueprint.route("/review/<int:acc_id>", methods=["GET"])
@login_required
def index(acc_id):
    print(f"acc_id: {acc_id}")

    followers = (
        User.select()
        .join(Account_follower, on=(User.id== Account_follower.follower))
        .where(
            (Account_follower.account==acc_id)
            &
            (Account_follower.approved == False)
        )
    )

    return render_template('followers/review_requests.html',followers=followers)

# Process follow requests
@followers_blueprint.route("/update_requests/<int:acc_id>/<int:follower_id>/status=<int:accept>", methods=["POST"])
@login_required
def update(acc_id,follower_id,accept):
    request = Account_follower.get((Account_follower.follower==follower_id) & (Account_follower.account_id==acc_id))
    follower=User.get_by_id(follower_id)

    if accept:
        request.approved=True
        
        if request.save():
            flash(f"You have accepted {follower.name}'s request!")
        else:
            flash("Unable to accept request")
            return render_template( 'home.html',errors=request.errors)

    else:
        request.delete_instance()
        flash(f"You have removed {follower.name}'s request.")
    return redirect(url_for('followers.index', acc_id=acc_id))

# Destroys follow request
@followers_blueprint.route("/delete_requests/<int:acc_id>/<int:follower_id>", methods=["POST"])
@login_required
def destroy(acc_id,follower_id):
    print("IN DESTROY")
    relationship = Account_follower.select().where((Account_follower.account==acc_id)&(Account_follower.follower==follower_id))

    for r in relationship:
        print(r.id)
        r.delete_instance()
        acc = User.get_by_id(acc_id)
    
    flash(f"You have removed your follow request to {acc.name}.")

    return redirect(url_for('home'))