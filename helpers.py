import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
from config import MERCHANT_ID, PUBLIC_KEY,PRIVATE_KEY
import braintree

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=MERCHANT_ID,
        public_key=PUBLIC_KEY,
        private_key=PRIVATE_KEY
    )
)