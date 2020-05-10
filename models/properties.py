import peewee as pw
from models.base_model import BaseModel
from models.user import User


class Property(BaseModel):
    name = pw.CharField(unique=True, null=False)
    user = pw.ForeignKeyField(User, backref='properties')
    houses = pw.IntegerField(default=0)
    mortgaged = pw.BooleanField(default=False)

    def validate(self):
        return
