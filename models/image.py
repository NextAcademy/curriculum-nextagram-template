from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    path = pw.CharField()
    user = pw.ForeignKeyField(User, backref = 'images')

    @hybrid_property
    def image_url(self):
        from instagram_web.util.helpers import S3_LOCATION
        return S3_LOCATION + self.path
