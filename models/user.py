import peewee as pw
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin
from flask import Flask, request, flash


class User(BaseModel, UserMixin):
    username = pw.CharField(null=False)
    email = pw.CharField(null=False)
    password = pw.CharField()

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        if duplicate_username and duplicate_username.id != self.id:
            self.errors.append("Username not unique.Please try again")
        duplicate_email = User.get_or_none(User.email == self.email)
        if duplicate_email and duplicate_email.id != self.id:
            self.errors.append("Email not unique.Please try again")
        # if len(self.password) < 7:
        #     self.errors.append(
        #         "Your password needs to be at least 7 characters.")
        # if not re.search(r)

        weird_pass = len(self.password) < 7
        bad_pass = re.search(
            r"[a-z]", self.password) and re.search(r"[A-Z]", self.password) and re.search(r"\W", self.password)

        if weird_pass:
            self.errors.append("Password needs to be at least 8 characters")
        if not bad_pass:
            self.errors.append(
                "Password needs to contain upper and lower case letters and special characters")
        else:
            username = request.form.get("username")
            user_exist = User.get_or_none(User.username == username)
            if user_exist:
                self.password = self.password
            else:
                self.password = generate_password_hash(self.password)
