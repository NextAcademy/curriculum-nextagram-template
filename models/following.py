from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Following(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='idol', on_delete="cascade")
    follower_id = pw.ForeignKeyField(User, backref='follower', on_delete="cascade")
    approved = pw.BooleanField(default=True)
