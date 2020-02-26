from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(uniqie=False, null=False)

    def validate(self):
        print(
            f"Username or email has already been registered.")
        return True
