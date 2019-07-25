from models.base_model import BaseModel
from models.user import User
from config import S3_HOST_URL
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    image_name = pw.CharField(null=False)
    caption = pw.CharField(null=True)

    @hybrid_property
    def image_url(self):
        return f"{S3_HOST_URL}/{self.image_name}"
