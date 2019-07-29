import os
import datetime
from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    first_name = pw.CharField(null=True)
    last_name = pw.CharField()
    email = pw.CharField(unique=True, null=False)
    username = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    photo = pw.CharField(null=True)
    private = pw.BooleanField(default=True)

    @hybrid_property
    def profile_picture_url(self):
        from instagram_web.util.helpers import S3_LOCATION
        if self.photo:
            return S3_LOCATION + self.photo
        else:
            return "https://afcm.ca/wp-content/uploads/2018/06/no-photo.png"

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_following(self, user):
        for idol in self.idols:
            if idol.idol_id == user:
                return True 

    # def validate_update(self, id):
    #     self.errors = []
    #     self.check_form()

    #     update_user = User.get_by_id(id)
    #     check_password = check_password_hash(update_user.password, self.password)

    #     if not check_password:
    #         self.errors.append('Incorrect password')

    #     if len(self.errors) == 0:
    #         return True
    #     else:
    #         return False


    def validate(self):
        self.check_form()
        duplicate_username = User.get_or_none(User.username == self.username)

        if len(self.username) < 4:
            self.errors.append('Please provide a longer username.')

        if duplicate_username:
            self.errors.append('Username is not available.')

    def check_form(self):
        duplicate_email = User.get_or_none(User.email == self.email)

        if len(self.password) < 6:
            self.errors.append('Please enter a longer password')
        else:
            self.password = generate_password_hash(self.password)

        if len(self.first_name) < 1:
            self.errors.append('Please enter a first name.')

        if len(self.last_name) < 1:
            self.errors.append('Please enter a last name.')

        if duplicate_email:
            self.errors.append('Provided email is already in use.')