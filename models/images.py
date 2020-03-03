import peewee as pw
from models.base_model import BaseModel
from flask_login import UserMixin
from flask import Flask, request, flash
from models.user import User
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    user_image = pw.CharField()

    @hybrid_property
    def full_image_url(self):
        return self.user_image

    @hybrid_property
    def total_donations(self):
        from models.donations import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount
        return round(total)
