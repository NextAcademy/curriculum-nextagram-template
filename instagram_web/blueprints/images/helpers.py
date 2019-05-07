from app import app
import boto3
import botocore
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
from config import S3_KEY, S3_SECRET, S3_LOCATION
from werkzeug import secure_filename

#allowed extensions#
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return f'{S3_LOCATION}{file.filename}'
