from models.base_model import BaseModel
import peewee as pw
from flask_login import current_user


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        if current_user.id != self.id:
            if duplicate_username:
                self.errors.append('Username taken. ')

            if duplicate_email:
                self.errors.append('Email has been registered.')
