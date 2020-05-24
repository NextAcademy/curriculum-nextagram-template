from models.base_model import BaseModel
from models.user import User
import peewee as pw
import re
from playhouse.hybrid import hybrid_property, hybrid_method


class FF(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")
