from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    email = pw.CharField(null=False)
    full_name = pw.CharField(null=False)
    username = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
