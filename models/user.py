from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class User(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False)
# add in signup aand password.

# -----------------FIGURE OUT VALIDATION AFTER ---

    def validate(self):
        # pattern = "[A-Za-z0-9@#$%^&+=]"

        regexcheck = re.match(
            r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$', self.password)

        if len(self.password) <= 6:
            self.errors.append('Password must be more than 6 characters')
        elif not (regexcheck):
            self.errors.append(
                'Password must have atleast the following: one uppercase letter, one lowercase letter, and one special character')
        else:
            self.password = generate_password_hash(self.password)
        # implement the validation from yesterday
        duplicate_email = User.get_or_none(User.email == self.email)
        # pass_check = User.get_or_none(User.password == self.password)
        if duplicate_email:
            self.errors.append('Email already taken')
        else:
            print('Validation is now being implemented')

        return True
