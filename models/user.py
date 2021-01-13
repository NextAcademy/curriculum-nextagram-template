from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=True) #username
    email=pw.CharField(unique=True)
    password=pw.CharField(unique=False, max_length=30)
    address=pw.TextField(unique=False, null=False, default=None)

    # validations:
    # [x] duplicates for name and email
    # password 
        # longer than 6 characters
        # both uppercase and lowercase characters
        # at least one special character (REGEX comes in handy here)
    def validate(self):
        duplicate = User.get_or_none(User.name==self.name, User.email==self.email )



        if duplicate:
            self.errors.append("Username or email is already taken. Please try again.")
