from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
import peewee as pw
from models.user import User

class Post(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='posts', on_delete="cascade")
    post_image = pw.CharField(unique=True) #this will be the filename
    #post_caption?

    @hybrid_property
    def post_url(self):
        from app import app
        return app.config['S3_LOCATION']+str(self.user_id)+'/'+self.post_image
