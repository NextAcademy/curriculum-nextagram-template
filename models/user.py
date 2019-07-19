from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash


class User(BaseModel):
    first_name = pw.CharField(null=True)
    last_name = pw.CharField()
    email = pw.CharField(unique=True, null=False)
    username = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        duplicate_username = User.get_or_none(User.username == self.username)

        if len(self.password) < 6:
            self.errors.append('Please enter a longer password')
        else:
            self.password = generate_password_hash(self.password)

        if len(self.first_name) < 1:
            self.errors.append('Please enter a first name.')

        if len(self.last_name) < 1:
            self.errors.append('Please enter a last name.')

        if len(self.username) < 4:
            self.errors.append('Please provide a longer username.')

        if duplicate_email:
            self.errors.append('Provided email is already in use.')

        if duplicate_username:
            self.errors.append('Username is not available.')