from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
#-------------------------------------------------
from flask_login import UserMixin
#-------------------------------------------------

class User(BaseModel,UserMixin):
    name = pw.CharField(unique=True) #username
    email=pw.CharField(unique=True)
    password=pw.TextField(unique=False)

    # Validation section
    def validate(self):
        self.email_check()
        self.duplicate_check()
        self.password_check()

    def email_check(self):
        email_split = self.email.split("@")
        if len(email_split[0]) < 2:
            self.errors.append("Email length is too short. Please check your email and try again.")

    def duplicate_check(self):
        duplicate_name = User.get_or_none(User.name==self.name)
        duplicate_email =  User.get_or_none(User.email==self.email)
        if duplicate_name:
            self.errors.append("Username is already taken. Please try again.")
        if duplicate_email:
            self.errors.append("Email is already taken. Please try again.")

    def password_check(self):
        error_flag = False

        special_char = re.search('[\W]', self.password)
        lowercase = re.search('[a-z]',self.password) 
        uppercase = re.search('[A-Z]',self.password) 
        number = re.search('[0-9]',self.password) 

        if len(self.password) <6:
            self.errors.append("Password must be longer than 6 characters")
            error_flag = True

        if not(special_char and lowercase and uppercase and number):
            self.errors.append("Password must have an uppercase letter, lowercase letter and at least one special character")
            error_flag = True

        # if not error_flag: # <--may not need this condition
        self.password = generate_password_hash(self.password)

    

