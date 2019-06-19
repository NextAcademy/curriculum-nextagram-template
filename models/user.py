from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_pic = pw.CharField(default="")
    is_private = pw.BooleanField(default = False)

    @hybrid_property
    def profile_image_url(self):
        from app import app
        if self.profile_pic != "":
            return app.config['S3_LOCATION']+str(self.id)+'/'+self.profile_pic
        return app.config['S3_LOCATION']+'default_profile_pic.jpg'

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username not unique')
        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email not unique')