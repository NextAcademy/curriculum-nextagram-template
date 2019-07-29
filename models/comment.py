from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw
from playhouse.hybrid import hybrid_property


class Comment(BaseModel):
    text = pw.CharField()
    user = pw.ForeignKeyField(User, backref = 'comments')
    image = pw.ForeignKeyField(Image, backref='comments')
