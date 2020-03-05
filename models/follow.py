from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Follow(BaseModel):
    fan = pw.ForeignKeyField(User, backref='fans')
    idol = pw.ForeignKeyField(User, backref='idols')

    def validate(self):
        return
