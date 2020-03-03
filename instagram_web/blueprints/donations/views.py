# from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
# from flask_login import login_required
# from flask_login import current_user
# from models.image import Image
# from models.donation import Donation

# donations_blueprint = Blueprint('donations',
#                                 __name__,
#                                 template_folder='templates')


# @donations_blueprint.route('/<image_id>/new', methods=['GET'])
# @login_required
# def new(image_id):
#     image = Image.get_or_none(Image.id == image_id)

#     if not image:
#         flash('No image found', 'warning')
#         return redirect(url_for('users.profilepage'))

#     client_token = gateway.client_token.generate()
#     if not client_token:
#         flash('Oh no', 'warning')
#         return redirect(url_for('users.profilepage'))

#     return render_template('donations/new.html', image=image)


# @donations_blueprint.route('/<image_id>/create', methods=['POST'])
# @login_required
# def create(image_id):
#     nonce = request.form.get('payment_method_nonce')
#     if not nonce:
#         flash('invalid credit card details', 'warning')
#         return redirect(url_for('users.profilepage'))

#     image = Image.get_or_none(Image.id == image_id)

#     if not image:
#         flash('No image found with the provided id', 'waning')
#         return redirect(url_for('users.profilepage'))

#     amount = request.form.get('amount')

#     if not amount:
#         flash('No donation amount provided', 'warning')
#         return redirect(url_for('users.profilepage'))

#     result = gateway.transaction.sale({
#         "amount": amount,
#         "payment_method_nonce": nonce,
#         "options" [
#             "submit_for_settlement": True
#         ]
#     })

#     if not result.is_success:
#         flash('Unable to complete transaction', 'warning')
#         return redirect(request.referrer)

#     donation = Donation(amount=amount, image_id=image.id,
#                         user_id=current_user.id)

#     if not donation.save():
#         flash('Donation successful but error creating record', 'waning')
#         return redirect(url_for('users.profilepage'))

#     flash('Donation successful. $(amount) donated', 'success')
#     return redirect(url_for(users.profilepage))
