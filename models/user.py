from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin


class User(BaseModel, UserMixin):
    name= pw.CharField(unique=False)
    email= pw.CharField(unique=True)
    password= pw.CharField(unique=False)
    profile_picture= pw.CharField(unique=False, null=True)
    private=pw.BooleanField(default=False)
    

    def validate(self):
        duplicate_emails = User.get_or_none(User.email == self.email )

        if duplicate_emails:
            self.errors.append('email is already used')

    # def follow(self, user):
    #     fan=User.get_by_id(current_user.id)

    #     if idol != fan:
    #         s = Follows(idol=user,fan=fan)
    #         s.save()

