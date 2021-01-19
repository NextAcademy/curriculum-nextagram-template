from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property
import peewee as pw

class Image(BaseModel):
    url=pw.CharField(null=False)
    # CASCADE --> when user is deleted, corresponding images are deleted too
    user=pw.ForeignKeyField(User, backref="images", on_delete="CASCADE") 

# ---------- NEW --------------
# ---------- Need to remove in html's  --------------
    # @hybrid_property
    # def full_image_path:
    #     from app import app
    #     return app.config.get("S3_LOCATION") +self.url