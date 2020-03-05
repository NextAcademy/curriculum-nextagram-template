from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property, hybrid_method


class User(BaseModel):
    name = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    profile_image = pw.CharField(null=True)

    @hybrid_method
    def is_following(self, user):
        from models.FF import FF
        return True if FF.get_or_none((FF.idol_id == user.id) & (FF.fan_id == self.id)) else False

    @hybrid_method
    def is_followed_by(self, user):
        from models.FF import FF
        return True if FF.get_or_none((FF.fan_id == user.id) & (FF.idol_id == self.id)) else False

    @hybrid_property
    def profile_image_url(self):

        return f"https://zeft-bucket.s3.ap-southeast-1.amazonaws.com/{self.profile_image}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def validate(self):

        dup_name = User.get_or_none(User.name == self.name)
        # dup_pass = User.get_or_none(User.name == self.name)
        dup_email = User.get_or_none(User.email == self.email)

        regexcheck = re.match(
            r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$', self.password)

        length_check = len(self.password) < 6
        # if not (regexcheck):
        #     self.errors.append(
        #         'Password must have at least the following: one uppercase letter, one lowercase letter, and one special character')

        if not self.id and length_check:
            self.errors.append(
                'PW must be > 6 ')

        if dup_name and not dup_name.id == self.id:
            self.errors.append('Username has been taken')

        if dup_email and not dup_email.id == self.id:
            self.errors.append('Email already exist')

        else:
            if not self.id:
                self.password = generate_password_hash(self.password)
        # if dup_pass = USer
        return True
