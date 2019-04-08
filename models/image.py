import os
from app import app
from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    image_path = pw.CharField(null=True)
    caption = pw.TextField(null=True)
    user = pw.ForeignKeyField(User, backref="images", index=True, null=True, on_delete="CASCADE")

    def validate(self):
        pass

    @hybrid_property
    def image_url(self):
        if self.image_path:
            return app.config['S3_LOCATION'] + self.image_path