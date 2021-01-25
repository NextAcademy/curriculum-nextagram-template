from app import app
from flask import render_template
from .util.assets import bundles
from flask_assets import Environment, Bundle
from flask_login import current_user
from instagram_web.util.google_oauth import oauth
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.followers.views import followers_blueprint

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(followers_blueprint, url_prefix="/followers")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'),403

@app.route("/")
def home():
    # pass a list of users and their uploaded images
    from models.user import User
    from models.account_follower import Account_follower
    user_list = User.select()

    # get current_user's followings
    # only display public profiles + private&approved

    # 1. Get all users current user is following
    # 2. if public, append to list
    # 3. if private and approved, append to list


    if current_user.is_anonymous:
        return render_template('home.html')

    else:
        viewer = User.get_by_id(current_user.id)
        following = viewer.get_following()
        user_list =[]

        for user in following:
            print (user.name, user.private)
            if not user.private:
                user_list.append(user)
            else:
                # if relationship approved, add to user_list
                relationship = (
                    Account_follower.get_or_none(
                        Account_follower.account == user.id, 
                        Account_follower.follower==current_user.id
                    )
                )
                if relationship.approved:
                    user_list.append(user)
        

    return render_template('home.html',user_list=user_list)
