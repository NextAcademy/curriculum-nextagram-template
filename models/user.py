from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username:
            self.errors.append('Username not unique')
        if duplicate_email:
            self.errors.append('Email not unique')
        if len(self.password) < 8:
            self.error.append('Password too short')
        else:
            self.password = generate_password_hash(self.password)