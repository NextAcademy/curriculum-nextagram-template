from models.base_model import BaseModel
import peewee as pw
import os



class User(BaseModel):
    first_name = pw.CharField()
    last_name = pw.CharField(null=True)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username:
            self.errors.append('Username has been registered. Please try another.')
        elif duplicate_email:
            self.errors.append('Email has been registered. Please try another.')

