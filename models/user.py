from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    email = pw.CharField(null=False)
    full_name = pw.CharField(null=False)
    username = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
