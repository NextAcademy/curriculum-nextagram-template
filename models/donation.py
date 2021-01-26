from models.base_model import BaseModel
import peewee as pw
from models.image import Image

class Donation(BaseModel):
    amount = pw.DecimalField(decimal_places=2)
    image = pw.ForeignKeyField(Image, backref="donations")