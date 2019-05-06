from models.base_model import BaseModel
from flask_login import LoginManager
import peewee as pw
import re


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)

    @classmethod
    def validate_password(self, password):
        valid_password = True
        while valid_password:
            if (len(password) < 6 or len(password) > 12):
                break
            elif not re.search("[a-z]", password):
                break
            elif not re.search("[A-Z]", password):
                break
            elif not re.search("[0-9]", password):
                break
            elif not re.search("[#@$!]", password):
                break
            elif re.search("\s", password):
                break
            else:
                valid_password = False
                break

        return valid_password

        if duplicate_username:
            self.errors.append(
                'Username is already taken. Please choose something else please.')

        else:
            flash("Username available!")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
