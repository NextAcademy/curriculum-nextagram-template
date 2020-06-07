import peewee as pw
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION


class Card(BaseModel):
    category = pw.CharField()
    image = pw.CharField(null=True)
    description = pw.CharField(null=True)

    @hybrid_property
    def image_url(self):
        return(S3_LOCATION + self.image)
