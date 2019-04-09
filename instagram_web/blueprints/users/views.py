from __future__ import print_function
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from models.idols_fans import Follows
from models.donation import Donation
from werkzeug.security import generate_password_hash
from  flask_login import current_user
from helpers import s3
from peewee import prefetch
from helpers import gateway
from money.money import Money
from money.currency import Currency
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import sys
   


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    s = User(name=request.form['name'], email=request.form['email'], password= generate_password_hash(request.form['password']))

    if s.save():
        flash("Successfully saved")
        return redirect(url_for("sessions.new"))
    else:
        return render_template('users/new.html', errors=s.errors)
    


@users_blueprint.route('/<name>', methods=["GET"])
def show(name):

    fans_count= User.select().join(Follows, on=(Follows.fan_id==User.id)).where(Follows.idol_id==current_user.id, Follows.approval==True).count()

    idols_count= User.select().join(Follows, on=(Follows.idol_id==User.id)).where(Follows.fan_id==current_user.id).count()


    return render_template('users/user_page.html', fans_count=fans_count, idols_count=idols_count)

@users_blueprint.route('/private/update', methods=['POST'])
def private_update():
    if current_user.private == False :
         s=(User.update({User.private: True}).where(User.id==current_user.id))
         s.execute()
    elif current_user.private ==True:
         s=(User.update({User.private: False}).where(User.id==current_user.id))
         s.execute()
    return redirect(url_for('users.show', name=current_user.name))


@users_blueprint.route('/user/<id>', methods=['GET'])
def show_user(id):
    user= User.get_by_id(id)
    following_status= False
    follow= Follows.select()

    if  user.private == True:
        if  follow.where(Follows.fan_id==current_user.id, Follows.idol_id==user.id, Follows.approval==False):
            following_status= "Pending"
            
            return render_template('users/other_user_page.html', user=user, following_status=following_status)

        
        elif  follow.where(Follows.fan_id==current_user.id, Follows.idol_id==user.id, Follows.approval==True):
            following_status= True
            
            return render_template('users/other_user_page.html', user=user, following_status=following_status)


    if follow.where(Follows.fan_id==current_user.id, Follows.idol_id==user.id):
        following_status=True
    return render_template('users/other_user_page.html', user=user, following_status=following_status)


@users_blueprint.route('/', methods=["GET"])
def index():

    users= User.select()
    user_images= Image.select()
    user_with_images= prefetch(users, user_images)
    follow= Follows.select()
    # status= follow.where(Follows.fan_id==current_user.id, Follows.idol_id==user.id, Follows.approval==True)

    return render_template('home.html', users=user_with_images, follow= follow, Follows=Follows)


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit_page.html',id=id)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    name = request.form['name']
    email = request.form['email']
    old_password = request.form['old_password']
    confirm_password = request.form['confirm_password']
    password = request.form['password']       

    if current_user == user and old_password == confirm_password:
        s=(User.update({User.name: name, User.email:email, User.password: generate_password_hash(password)}).where(User.id == id))
        s.execute()
        return redirect (url_for('users.show', name=user.name))
    else:
        return "nothing"
   
@users_blueprint.route('/<id>/profile_pic/edit', methods=['GET'])
def profile_pic_edit(id):
    return render_template('users/profilepic_edit_page.html', id = id)

@users_blueprint.route('/<id>/profile_pic/update', methods=['POST'])
def profile_pic_update(id):

    file=request.files.get("user_file")
    s=(User.update({User.profile_picture: file.filename}).where(User.id==id))
    s.execute()
    s3.upload_fileobj(
        file,
        "nextagramtao",
        file.filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )
    return redirect(url_for('users.show', name= current_user.name))

@users_blueprint.route('/<id>/upload_image/edit', methods=['GET'])
def upload_image(id):
    return render_template('users/upload_image.html', id=id)

@users_blueprint.route('<id>/upload_image/update', methods=['POST'])
def upload_image_update(id):
    file=request.files.get("user_file")
    s = Image(user=id,image_url=file.filename)
    s.save()
    s3.upload_fileobj(
        file,
        "nextagramtao",
        file.filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )
    return redirect(url_for('users.show', name=current_user.name))

@users_blueprint.route("/client_token", methods=["GET"])
def client_token():
     client_token= gateway.client_token.generate()
     return render_template('users/payment_form.html',client_token=client_token, image_id=request.args["image_id"] )

@users_blueprint.route("/checkout", methods=["POST"])
def create_purchase():
    nonce_from_the_client = request.form["payment_method_nonce"]
    amount_paid= request.form['amount_paid']
    s = Donation(amount=amount_paid,user=current_user.id,image=request.form["image_id"])
    s.save()

    result = gateway.transaction.sale({
    "amount": amount_paid,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }})

    message = Mail(
    from_email='from_email@example.com',
    to_emails='seowyongtao96@gmail.com',
    subject='Sending with SendGrid is Fun',
    html_content=f'<strong>you donate{amount_paid}to nextagram.Thank you !</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return redirect(url_for('users.index'))


@users_blueprint.route("/<id>/follow/update", methods=["POST"])
def follow_update(id):
    idol= User.get_by_id(id)
    fan=User.get_by_id(current_user.id)
   
    # cannot follow ownself
    if idol != fan:
        s = Follows(idol=idol,fan=fan)
        s.save()

    return redirect(url_for('users.show_user', id= idol.id))

@users_blueprint.route("/<id>/unfollow/update", methods=["POST"])
def unfollow_update(id):
    idol= User.get_by_id(id)
    fan=User.get_by_id(current_user.id)

    q= Follows.delete().where(Follows.idol_id==idol.id, Follows.fan_id==fan.id)
    q.execute()


    return redirect(url_for('users.show_user', id= idol.id))

@users_blueprint.route("/friend_requests", methods=["GET"])
def show_friend_request():

        
        fans= User.select().join(Follows, on=(Follows.fan_id==User.id)).where(Follows.idol_id==current_user.id, Follows.approval==False)

        # breakpoint()
        return render_template('users/request_page.html', fans=fans)

@users_blueprint.route("/<id>/accept", methods=["POST"])
def follow_accept(id):
    idol= User.get_by_id(current_user.id)
    fan=User.get_by_id(id)

    s=(Follows.update({Follows.approval: True}).where(Follows.idol_id==idol.id, Follows.fan_id==fan.id))
    s.execute()
    
    
    
    fans= User.select().join(Follows, on=(Follows.fan_id==User.id)).where(Follows.idol_id==current_user.id, Follows.approval==False)
    return render_template('users/request_page.html', fans=fans)

@users_blueprint.route("/<id>/reject", methods=["POST"])
def follow_reject(id):
    idol= User.get_by_id(current_user.id)
    fan=User.get_by_id(id)

    s=(Follows.delete().where(Follows.idol_id==idol.id, Follows.fan_id==fan.id))
    s.execute()

    fans= User.select().join(Follows, on=(Follows.fan_id==User.id)).where(Follows.idol_id==current_user.id, Follows.approval==False)
    return render_template('users/request_page.html', fans=fans)


    


    






   

    
