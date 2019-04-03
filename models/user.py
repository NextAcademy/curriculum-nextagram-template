import os
from models.base_model import BaseModel
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
import peewee as pw
from app import app

class User(UserMixin, BaseModel):
    name = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    username = pw.CharField(unique=True, index=True, null=False)
    profile_image_path = pw.CharField(null=True)


    @hybrid_property
    def profile_image_url(self):
        if self.profile_image_path:
            return app.config['S3_LOCATION'] + self.profile_image_path
        else:
            return app.config['S3_LOCATION'] + "26_profile-placeholder.png2019-04-03_104711.587724"