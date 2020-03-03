import peewee as pw
from models.base_model import BaseModel
from models.images import Image
from models.user import User


class Donation(BaseModel):
    amount = pw.DecimalField()
    image = pw.ForeignKeyField(Image, backref="donations")
    user = pw.ForeignKeyField(User, backref="donations")
