from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Image(BaseModel):
    url=pw.CharField(null=False)
    user=pw.ForeignKeyField(User, backref="images")
