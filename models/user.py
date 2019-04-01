from models.base_model import BaseModel
import peewee as pw

# from flask_wtf import FlaskForm

class User(BaseModel):
    first_name = pw.CharField()
    last_name = pw.CharField(null=True)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()