from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_username:
            self.errors.append(
                'Username is already taken. Please choose something else.')

        else:
            flash("Username available!")
