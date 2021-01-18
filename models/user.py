from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique = True, null=False)
    password_hash = pw.TextField(null=False)
    password = None

    def validate(self):
        # check if email is unique
        existing_user_email = User.get_or_none(User.email == self.email)
        if existing_user_email:
            self.errors.append(f"User with {self.email} already exists")

        # username should be unique
        existing_user_username =  User.get_or_none(User.username == self.username)
        if existing_user_username:
            self.errors.append(f"User with {self.username} already exists")

        # password validations
        if len(self.password) <= 6:
            self.errors.append("Password is less than 6 characters")
        # lowercase characters & uppercase characters 
        has_lower = re.search(r"[a-z]", self.password)
        has_upper = re.search(r"[A-Z]", self.password)
        has_special = re.search(r"[\[ \] \@ \$ \* \^ \# \%]", self.password)

        if has_lower and has_upper and has_special:
            self.password_hash = generate_password_hash(self.password)
        else:
            self.errors.append("Password either does not have lower, upper, or special characters")


