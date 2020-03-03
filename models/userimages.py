# MODEL FOR USER IMAGES
from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

# ONE USER CAN HAVE MANY IMAGES.


class UserImage(BaseModel):
    user = pw.ForeignKeyField(User, backref='userimages')
    user_image = pw.CharField(null=True)
    caption = pw.CharField(null=True)

    @hybrid_property
    def user_image_url(self):
        # if changed provider, just need to change the url
        if self.user_image:
            return f"https://nextacademyhf.s3-ap-southeast-1.amazonaws.com/{self.user_image}"

    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount

        return round(total)

    #     return round(total)
    # def validate(self):
    #     existing_username = UserImage.get_or_none(
    #         UserImage.user_id == self.user_id)
    #     if existing_username and not existing_username.id == self.id:
    #         self.errors.append('Username already taken')
