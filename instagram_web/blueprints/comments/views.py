import peewee
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user
from models.comment import Comment
from instagram_web.util.helpers import allowed_file, upload_file_to_s3


comments_blueprint = Blueprint('comments',
                            __name__,
                            template_folder='templates')

@comments_blueprint.route('/', methods=['POST'])
def create():
    text = request.form.get('text')
    image = request.form.get('image')

    comment= Comment(text=text, user_id=current_user.id, image_id=image)

    if comment.save():
        flash('Thank you for your comment', 'success')
    else:
        flash('Sorry, something went wrong. Try again.', 'danger')

    return redirect(url_for('images.show', id=image))


@comments_blueprint.route('/<id>', methods=['POST'])
def delete(id):
    image = request.form.get('image')
    comment = Comment.get_by_id(id)
    comment.delete_instance()

    flash('Your comment has been removed', 'info')
    return redirect(url_for('images.show', id=image))


