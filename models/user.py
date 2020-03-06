import peewee as pw
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property, hybrid_method
import re
from flask_login import UserMixin
from flask import Flask, request, flash


class User(BaseModel, UserMixin):
    username = pw.CharField(null=False)
    email = pw.CharField(null=False)
    password = pw.CharField()
    profile_image = pw.CharField(null=True)
    # caption = pw.CharField(null=True)

    @hybrid_property
    def profile_image_url(self):
        return f"https://jynmunbucket.s3-ap-southeast-1.amazonaws.com/{self.profile_image}"

    @hybrid_property
    def followers(self):
        from models.follower_following import FollowerFollowing
        return [user.idol for user in FollowerFollowing.select().where(FollowerFollowing.fan_id == self.id)]

    @hybrid_property
    def following(self):
        from models.follower_following import FollowerFollowing
        return [user.fan for user in FollowerFollowing.select().where(FollowerFollowing.idol_id == self.id)]

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False

    @hybrid_method
    def is_followed_by(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.fan_id == user.id) & (FollowerFollowing.idol_id == self.id)) else False

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
                if not self.id:
                    self.password = generate_password_hash(self.password)
