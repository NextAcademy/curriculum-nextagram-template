from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property


class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique = True, null=False)
    password_hash = pw.TextField(null=False)
    password = None
    image_path = pw.TextField(null=True)
    is_private = pw.BooleanField(default=False)

    def follow(self, idol):
        from models.fanidol import FanIdol
        # check if the relationship exists
        if self.follow_status(idol) == None:
            relationship = FanIdol(idol=idol, fan=self.id)
            if not idol.is_private:
                relationship.is_approved = True
            return relationship.save()
        else:
            return 0

    def unfollow(self, idol):
        from models.fanidol import FanIdol
        return FanIdol.delete().where(FanIdol.fan == self.id, FanIdol.idol == idol).execute()

    def follow_status(self, idol):
        from models.fanidol import FanIdol
        return FanIdol.get_or_none(FanIdol.fan == self.id, FanIdol.idol == idol.id)


    @hybrid_property
    def idols(self):
        from models.fanidol import FanIdol
        # get a list of idols
        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan == self.id, FanIdol.is_approved == True)
        return User.select().where(User.id.in_(idols))

        # --- ANOTHER WAY OF DOING THE ABOVE ---
        # user_idol = []
        # for row in idols:
            # user_idol.append(row.idol)
        # return user.idol

    @hybrid_property
    def fans(self):
        from models.fanidol import FanIdol
        # get a list of fans 
        fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol == self.id, FanIdol.is_approved == True)
        return User.select().where(User.id.in_(fans))

    @hybrid_property
    def idol_requests(self):
        from models.fanidol import FanIdol
        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan == self.id, FanIdol.is_approved == False)
        return User.select().where(User.id.in_(idols))

    @hybrid_property
    def fan_requests(self):
        from models.fanidol import FanIdol
        fans = FanIdol.select(FanIdol.fan).where(FanIdol.idol == self.id, FanIdol.is_approved == False)
        return User.select().where(User.id.in_(fans))

    @hybrid_property
    def approve_request(self, fan):
        from models.fanidol import FanIdol
        # get the relationship 
        relationship = fan.follow_status(self)
        relationship.is_approved = True
        return relationship.save()

    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            return ""

    def validate(self):
        # check if email is unique
        existing_user_email = User.get_or_none(User.email == self.email)
        if existing_user_email and existing_user_email.id !=self.id:
            self.errors.append(f"User with {self.email} already exists")

        # username should be unique
        existing_user_username =  User.get_or_none(User.username == self.username)
        if existing_user_username and existing_user_username.id !=self.id:
            self.errors.append(f"User with {self.username} already exists")

        # password validations
        if self.password:
            if len(self.password) <= 6:
                self.errors.append("Password is less than 6 characters")
            # lowercase characters & uppercase characters 
            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\[ \] \@ \$ \* \^ \# \%]", self.password)

            if has_lower and has_upper and has_special:
                self.password_hash = generate_password_hash(self.password)
            else:
                self.errors.append("Password either does not have lower, upper, or special characters")


