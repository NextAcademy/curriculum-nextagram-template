import peewee as pw
from models.base_model import BaseModel
from models.photos import Photos
from models.user import User


class Donation(BaseModel):
    amount = pw.DecimalField()
    photo = pw.ForeignKeyField(Photos, backref="donations")
    user = pw.ForeignKeyField(User, backref="donations")
