from models.base_model import BaseModel
import peewee as pw
from models.user_images import Image


class Comment(BaseModel):
    text = pw.TextField(unique=False, null=False)
    image = pw.ForeignKeyField(Image, backref='comments')

    def validate(self):
        return
