# Middle table of accounts and their followers

from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Account_follower(BaseModel):
    account= pw.ForeignKeyField(User, backref='accounts_following')
    follower= pw.ForeignKeyField(User, backref='followers')
    approved=pw.BooleanField(default=False) #False = pending approval, True = approved, and non-existent = Declined/no request yet

    def validate(self):
        # check if same relationship already exists

        # 1. get all relationships for this account:
        relationships = Account_follower.select().where(Account_follower.account==self.account)
        # 2. check all the followers for this account
        for r in relationships:
            print(r.account)
            if (self.approved==r.approved) and (self.account==r.account) and (self.follower==r.follower): # if no difference at all
                self.errors.append("You are already following this account.")
