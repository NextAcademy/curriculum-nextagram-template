import os
import peewee as pw
import datetime
from database import db
import os
from peewee_validates import ModelValidator

class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()
        validator = self.CustomValidator(self)
        validator.validate()

        if validator.errors != 0:
            for error in validator.errors.values():
                self.errors.append(error)

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    # def validate(self):
    #     print(
    #         f"Warning validation method not implemented for {str(type(self))}")
    #     return True

    class CustomValidator(ModelValidator):
        class Meta:
            messages = {}

    class Meta:
        database = db
        legacy_table_names = False
