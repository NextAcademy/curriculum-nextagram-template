import re
import peewee as pw
from flask_login import UserMixin
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property
# from models.account_follower import Account_follower
from werkzeug.security import generate_password_hash

class User(BaseModel,UserMixin):
    name = pw.CharField(unique=True ) #username
    email=pw.CharField(unique=True )
    password=pw.TextField(unique=False)
    profile_photo=pw.CharField(null=False, default="")
    private=pw.BooleanField(null=False, default="True")

    @hybrid_property
    def full_profile_photo(self):
        if self.profile_photo:
            from config import S3_LOCATION
            
            return S3_LOCATION + self.profile_photo
        else:
            return ""

    def get_photos(self):
        from models.image import Image
        image_list = pw.prefetch(Image.select().where(Image.user_id==self.id),User)
        return image_list

    
    # Ideally, place the logic as functions:
    # def follow(self, account):
    #     pass
    
    # def unfollow(self,account):
    #     from models.account_follower import Account_follower
    #     pass

    def get_followers(self):
        # Get followers of self's account
        from models.account_follower import Account_follower
        followers = Account_follower.select().where(Account_follower.account==self.id)
        return followers

    def get_following(self):
        # Get accounts self is following
        from models.account_follower import Account_follower
        accounts = (
            User.select()
            .join(Account_follower, on=(User.id==Account_follower.account))
            .where(Account_follower.follower==self.id)
        )

        return accounts

    # def follow_exists(self, account):
    #     from models.account_follower import Account_follower
    #     return Account_follower.get_or_none(Account_follower.account = account, Account_follower.follower=self.id)

    # def approve_follow(self,follower):
    #     pass
    
    # def reject_follow(self,follower):
    #     pass

    # List of account who follows self + to review
    # def get_followers_tba(self):
    #     from models.account_follower import Account_follower
    #     followers =(
    #         User.select()
    #         .join(Account_follower,on=(User.id==Account_follower.follower))
    #         .where(
    #             (Account_follower.acc_id==self.id)
    #             &
    #             (Account_follower.approved==False)
    #         )
    #     )
    #     return followers



    # List of account who follows self + approved    
    # def get_followers_approved(self):
    #     from models.account_follower import Account_follower
    #     followers=(
    #         User.select()
    #         .join(Account_follower,on=(User.id==Account_follower.follower))
    #         .where(
    #             (Account_follower.acc_id==self.id)
    #             &
    #             (Account_follower.approved==True)
    #         )
    #     )

    # List of account self is following
    # def get_following(self):
    #     from models.account_follower import Account_follower
    #     following = (
    #         User.select()
    #         .join(Account_follower,on=(User.id==Account_follower.acc_id))
    #         .where(
    #             (Account_follower.follower==self.id)
    #             &
    #             (Account_follower.approved==True)
    #         )
    #     )


    # Validation section
    def validate(self):
        self.duplicate_check()

        if self.email:
            self.email_check()

        if self.password:
            if not (self.password[0:19] == "pbkdf2:sha256:50000"): # if password is not changed
                self.password_check() # to verify if logic still works for changing password

    def email_check(self):
        email_split = self.email.split("@")
        if len(email_split[0]) < 2:
            self.errors.append("Email length is too short. Please check your email and try again.")
    def duplicate_check(self):
        duplicate_name = User.get_or_none(User.name==self.name)
        duplicate_email =  User.get_or_none(User.email==self.email)
        
        if duplicate_name: # if duplicate_name exists
            if not duplicate_name.id==self.id: #if the id is not your own
                self.errors.append("Username is already taken. Please try again.")

        if duplicate_email: # if duplicate_email exists
            if not duplicate_email.id==self.id: #if the id is not your own
                self.errors.append("Email is already taken. Please try again.")
    def password_check(self):
        error_flag = False

        special_char = re.search('[\W]', self.password)
        lowercase = re.search('[a-z]',self.password) 
        uppercase = re.search('[A-Z]',self.password) 
        number = re.search('[0-9]',self.password) 

        if len(self.password) <6:
            self.errors.append("Password must be longer than 6 characters")
            error_flag = True

        if not(special_char and lowercase and uppercase and number):
            self.errors.append("Password must have an uppercase letter, lowercase letter and at least one special character")
            error_flag = True

        if (self.password[0:19] == "pbkdf2:sha256:50000"): # hashed password
            pass
        else:
            self.password = generate_password_hash(self.password)

    

