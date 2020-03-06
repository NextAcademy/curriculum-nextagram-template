import peewee as pw
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
from models.user import User


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols')
    idol = pw.ForeignKeyField(User, backref='fans')

    class Meta:
        indexes = ((('fan', 'idol'), True),)
