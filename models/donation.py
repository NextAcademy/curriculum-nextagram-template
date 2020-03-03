from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.userimages import UserImage


class Donation(BaseModel):
    amount = pw.DecimalField()
    # get all donations associated to the image
    image = pw.ForeignKeyField(UserImage, backref="donations")
    # get all donations that user has made
    user = pw.ForeignKeyField(User, backref="donations")
