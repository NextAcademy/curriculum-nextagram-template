from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from playhouse.postgres_ext import PostgresqlExtDatabase
from sqlalchemy.ext.hybrid import hybrid_property
import os


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    password = pw.CharField()
    email = pw.CharField(unique=True)
    picture = pw.CharField(default='')

    def hash_password(self):
        self.password =  generate_password_hash(self.password)

    def followers(self):
        return User.select().join(Follows, on=Follows.myfan).where(Follows.myidol == self)

    def following(self):
        return User.select().join(Follows, on=Follows.myidol).where(Follows.myfan == self)


    # Hybrid properties to make sure user can can access profile image url like this: user.profile_image_url
    @hybrid_property
    def profile_image_url(self):
        return os.environ.get("S3_LOCATION") + self.picture

#     #Only authenticated users will fulfill the criteria of login_required.
#     def is_authenticated(self):
#         return True

#    #they also have activated their account, ex: the user able to send message to user email account
#     def is_active(self):
#         return True

#     #this is an anonymous user
#     def is_anonymous(self):
#         return True
 
#     #This method must return a unicode that uniquely identifies this user, 
#     # and can be used to load the user from the user_loader callback
#     def get_id(self):
#         return self.id 

class Images(BaseModel):
    user = pw.ForeignKeyField(User, backref='post')
    image_url = pw.TextField()
    pictures = pw.CharField(default='')

    # Hybrid properties to make sure user can can access post image url like this: user.profile_image_url
    @hybrid_property
    def post_image_url(self):
        return os.environ.get("S3_LOCATION") + self.image_url


class Follows(BaseModel):
    myfan = pw.ForeignKeyField(User, backref='myidol_id')
    myidol = pw.ForeignKeyField(User, backref='myfan_id')
    follow_status = pw.BooleanField(default = False)

class Payments(BaseModel):
    user = pw.ForeignKeyField(User, backref='donate_user')
    image = pw.ForeignKeyField(Images, backref="donate_image")
    amount = pw.DecimalField(default='')



    