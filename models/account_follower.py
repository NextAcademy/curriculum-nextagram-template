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
        relationships = Account_follower.select().where(Account_follower.account_id==self.account)
        # 2. check all the followers for this account
        for r in relationships:
            if self.id==r.id: #referring to same row in Account_follower table
                if self.approved == r.approved: # if there are no changes to approved status
                    print("Self.approved:")
                    print(self.approved)
                    print("r.approved:")
                    print(r.approved)
                    self.errors.append("You are already following this account.")
