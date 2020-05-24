from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property


class Photos(BaseModel):
    user = pw.ForeignKeyField(User, backref="images")
    filename = pw.CharField(null=False)
    caption = pw.CharField(null=True)

    @hybrid_property
    def image_url(self):
        return f"https://zeft-bucket.s3.ap-southeast-1.amazonaws.com/{self.filename}"

    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.photo_id == self.id):
            total = total + donation.amount
        return round(total)
