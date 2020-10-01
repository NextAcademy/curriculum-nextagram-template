from models.base_model import BaseModel
import peewee as pw
from models.user_images import Image


class Donation(BaseModel):
    amount = pw.DecimalField()
    image = pw.ForeignKeyField(Image, backref='donations')

    def validate(self):
        return
