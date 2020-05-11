import peewee as pw
from models.base_model import BaseModel


class ActivityLog(BaseModel):
    text = pw.TextField()

    def validate(self):
        return
