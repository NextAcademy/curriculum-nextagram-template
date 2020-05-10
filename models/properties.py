import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property


class Property(BaseModel):
    name = pw.CharField(unique=True, null=False)
    houses = pw.IntegerField(default=0)
    mortgaged = pw.BooleanField(default=False)
    user = pw.ForeignKeyField(User, backref='properties')

    def validate(self):
        return

    @hybrid_property
    def is_owned(self):
        if self.user.username == 'Banker':
            return False
        else:
            return True
