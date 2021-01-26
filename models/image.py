from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from models.user import User

class Image(BaseModel):
    image_url = pw.TextField(null=False)
    user = pw.ForeignKeyField(User, backref="images", on_delete="CASCADE")

@hybrid_property
def full_image_path(self):
    from app import app
    return app.config.get("S3_LOCATION") + self.image_url
