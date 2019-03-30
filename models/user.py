from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name= pw.CharField(unique=False)
    email= pw.CharField(unique=True)
    password= pw.CharField(unique=False)

    def validate(self):
        duplicate_emails = User.get_or_none(User.email == self.email )

        if duplicate_emails:
            self.errors.append('email is already used')


