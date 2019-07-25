from models.base_model import BaseModel
import peewee as pw
import re
from config import S3_HOST_URL
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    email = pw.CharField(null=False)
    full_name = pw.CharField(null=False)
    username = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    website = pw.CharField(null=True)
    bio = pw.TextField(null=True)
    phone_number = pw.CharField(null=True)
    profile_picture = pw.CharField(null=True)

    def validate(self):
        email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", self.email)
        password_valid = re.match(r"^[a-zA-Z]\w{3,14}$", self.password)
        duplicate_username = User.get_or_none(User.username == self.username)

        if not User.get_or_none(User.id == self.id):

            if len(self.full_name) < 1:
                self.errors.append('Please provide a name!')

            if not email_valid:
                self.errors.append('Invalid Email Provided')

            if duplicate_username:
                self.errors.append('Username already taken!')

            if password_valid:
                self.password = generate_password_hash(self.password)
            else:
                self.errors.append('Password is not valid, min 6 characters')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @hybrid_property
    def profile_url(self):
        return f"{S3_HOST_URL}/{self.profile_picture}"
