from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    first_name = pw.CharField(unique=False)
    last_name = pw.CharField(unique=False, null=True)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)