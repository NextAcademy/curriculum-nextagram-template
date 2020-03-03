import braintree
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BT_MERCHANT"),
        public_key=os.environ.get("BT_PUBLIC"),
        private_key=os.environ.get("BT_PRIVATE")
    )
)
