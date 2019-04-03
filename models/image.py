from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Image(BaseModel ):
    user= pw.ForeignKeyField(User, backref='images')
    image_url = pw.CharField(unique=False)