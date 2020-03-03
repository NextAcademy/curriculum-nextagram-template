import braintree
from braintree import BraintreeGateway, Configuration, Environment
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv("BT_MERCHANT_ID"),
        public_key=os.getenv("BT_PUBLIC_KEY"),
        private_key=os.getenv("BT_PRIVATE_KEY")

    )
)
