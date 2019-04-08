from app import app
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
from flask_login import UserMixin
import peewee as pw

class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    username = pw.CharField(unique=True, index=True, null=False)
    profile_image_path = pw.CharField(null=True)
    

    def validate(self):
        if self.name == "":
            self.errors.append('Name cannot be blank!')
        if len(self.username) < 6:
            self.errors.append('Username must be more than 6 characters!')
        if len(self.password) < 6:
            self.errors.append('Password must be more than 6 characters!')
        print(
            f"Warning validation method not implemented for {str(type(self))}")
        return True

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image_path:
            return app.config['S3_LOCATION'] + self.profile_image_path
        else:
            return app.config['S3_LOCATION'] + "26_profile-placeholder.png2019-04-03_104711.587724" 