from app import app
import os
import braintree
import config

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

gateway = braintree.BraintreeGateway(
   braintree.Configuration(
       braintree.Environment.Sandbox,
       merchant_id=os.environ['BT_MERCHANT_ID'] ,
       public_key=os.environ['BT_PUBLIC_KEY'],
       private_key=os.environ['BT_PRIVATE_KEY']
   )
)

def generate_client_token():
   return gateway.client_token.generate()

def transact(options):
   return gateway.transaction.sale(options)

def find_transaction(id):
   return gateway.transaction.find(id)