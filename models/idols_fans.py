from models.base_model import BaseModel
from models.user import User
import peewee as pw



class Follows(BaseModel):
    idol= pw.ForeignKeyField(User)
    fan= pw.ForeignKeyField(User)
    approval= pw.BooleanField(default=False)