from models.base_model import BaseModel
import peewee as pw
from flask_login import current_user
from config import S3_LOCATION
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    image = pw.CharField(unique=False, null=True,
                         default=S3_LOCATION + 'default-profile-image.png')

    @hybrid_property
    def is_followed(self):
        from models.follow import Follow
        followed = Follow.get_or_none(
            (Follow.fan_id == current_user.id) & (Follow.idol_id == self.id))

        return followed

    @hybrid_property
    def requests(self):
        from models.follow import Follow
        req = Follow.select().where(
            (Follow.idol_id == current_user.id) & (Follow.authorized == False))

        return req

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        if not current_user.is_authenticated:
            if duplicate_username:
                self.errors.append('Username taken. ')

            if duplicate_email:
                self.errors.append('Email has been registered.')
