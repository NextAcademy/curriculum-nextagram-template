from models.base_model import BaseModel
import peewee as pw
from flask_login import current_user
from playhouse.hybrid import hybrid_property


class Mon_User(BaseModel):
    name = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    position = pw.IntegerField(unique=False, default=0)
    properties = pw.TextField(null=True)
    money = pw.IntegerField(default=0)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def validate(self):
        duplicate_name = Mon_User.get_or_none(
            Mon_User.name == self.name)

        if not current_user.is_authenticated:
            if duplicate_name:
                self.errors.append('Username taken.')
