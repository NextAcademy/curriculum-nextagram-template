import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
import os


s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv('S3_KEY'),
   aws_secret_access_key=os.getenv('S3_SECRET')
)



def upload_file_to_s3(file, bucket_name, acl="public-read"):
    # breakpoint()

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
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return "{}{}".format(os.environ.get("S3_LOCATION"), file.filename)