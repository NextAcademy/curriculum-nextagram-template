from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Image(BaseModel):
    source = pw.CharField(unique=False, null=False)
    user = pw.ForeignKeyField(User, backref='images')

    def validate(self):
        return
