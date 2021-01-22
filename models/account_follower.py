# Middle table of accounts and their followers

from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Account_follower(BaseModel):
    account= pw.ForeignKeyField(User, backref='accounts_following')
    follower= pw.ForeignKeyField(User, backref='followers')
    status=pw.BooleanField(default=False) #False = pending approval, True = approved, and non-existent = Declined/no request yet

    # Place these functions here or in User model?
    def count_followers(self, acc):
        # Sum the total number of followers for this account
        pass

    def count_following(self, acc):
        # Provides list of users this account is following
        pass