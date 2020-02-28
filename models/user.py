from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    name = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    email = pw.CharField(unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def validate(self):
        dup_name = User.get_or_none(User.name == self.name)
        # dup_pass = User.get_or_none(User.name == self.name)
        dup_email = User.get_or_none(User.email == self.email)

        regexcheck = re.match(
            r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$', self.password)

        length_check = len(self.password) > 6
        # if not (regexcheck):
        #     self.errors.append(
        #         'Password must have at least the following: one uppercase letter, one lowercase letter, and one special character')

        if not length_check or not regexcheck:
            self.errors.append(
                'PW must be > 8 and include 1 lowercase, 1 uppercase and 1 special character')
        else:
            self.password = generate_password_hash(self.password)

        if dup_name:
            self.errors.append('Username has been taken')

        if dup_email:
            self.errors.append('Email already exist')

        # if dup_pass = USer
