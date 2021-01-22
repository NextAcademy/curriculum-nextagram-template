from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
#-------------------------------------------------
from flask_login import UserMixin
#-------------------------------------------------

class User(BaseModel,UserMixin):
    name = pw.CharField(unique=True ) #username
    email=pw.CharField(unique=True )
    password=pw.TextField(unique=False)
    profile_photo=pw.CharField(null=False, default="")
    private=pw.BooleanField(null=False, default="True")

    # Validation section
    def validate(self):
        self.duplicate_check()

        if self.email:
            self.email_check()

        if self.password:
            if not (self.password[0:19] == "pbkdf2:sha256:50000"): # if password is not changed
                self.password_check() # to verify if logic still works for changing password


    def email_check(self):
        email_split = self.email.split("@")
        if len(email_split[0]) < 2:
            self.errors.append("Email length is too short. Please check your email and try again.")

    def duplicate_check(self):
        duplicate_name = User.get_or_none(User.name==self.name)
        duplicate_email =  User.get_or_none(User.email==self.email)
        
        if duplicate_name: # if duplicate_name exists
            if not duplicate_name.id==self.id: #if the id is not your own
                self.errors.append("Username is already taken. Please try again.")

        if duplicate_email: # if duplicate_email exists
            if not duplicate_email.id==self.id: #if the id is not your own
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

        if (self.password[0:19] == "pbkdf2:sha256:50000"): # hashed password
            pass
        else:
            self.password = generate_password_hash(self.password)

    

