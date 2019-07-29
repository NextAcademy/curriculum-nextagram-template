from models.base_model import BaseModel
from models.user import User
import peewee as pw


class FanIdol(BaseModel):
    fan = pw.ForeignKeyField(User, backref = 'idols')
    idol = pw.ForeignKeyField(User, backref = 'fans')
    approved = pw.BooleanField(default=False)


