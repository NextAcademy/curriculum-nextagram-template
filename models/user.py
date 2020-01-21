from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    name = pw.CharField(unique=False, null=False, default='')
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        valid_email = re.match(email_regex, self.email)
        upper = False
        lower = False
        special = False
        for l in self.password:
            if l.isupper():
                upper = True
            elif l.islower():
                lower = True
            elif not(l.isalnum()):
                special = True
        pw_upper_lower_special = upper & lower & special
        # pw_special_character = re.search(r'\W', self.password)
        if len(self.password)<6 or not(pw_upper_lower_special):
            self.errors.append('Your password must be at least 6 characters long and contain an upper case letter, a lower case letter and a special character')
        else:
            self.password = generate_password_hash(self.password)
        if len(self.username)<6:
            self.errors.append('Your username must be at least 6 characters')

        if duplicate_username:
            self.errors.append('That username has already been taken')
       
        if duplicate_email:
            self.errors.append('That email has already been registered')

        if not(valid_email):
            self.errors.append('That email address is invalid')

         