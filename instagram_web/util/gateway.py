import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="j2gymnxpfwpyrn6r",
        public_key="4shn9gxdzpj4pt67",
        private_key="621c9e9059f0dfb50311ee141503b18d"
    )
)

client_token = gateway.client_token.generate({
})
