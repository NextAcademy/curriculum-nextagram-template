from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

class Donation(BaseModel ):
    amount=pw.DecimalField(unique=False)
    user= pw.ForeignKeyField(User, backref='donation')
    image = pw.ForeignKeyField(Image, backref='donation')