import peewee as pw
from models.base_model import BaseModel
from flask_login import UserMixin
from flask import Flask, request, flash
from models.user import User


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    user_image = pw.CharField()

    # @hybrid_property
    # def full_image_url(self):
    #     return
