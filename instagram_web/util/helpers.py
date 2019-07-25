import os
import boto3, botocore

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_KEY")
S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print(f"Somthing Happened: {e}")
        return e

    return f"{S3_LOCATION}{file.filename}"