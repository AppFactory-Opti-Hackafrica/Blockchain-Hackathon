import stellar_sdk
import requests

server = stellar_sdk.Server()

SQKeypair = stellar_sdk.Keypair.from_secret(input("Stellar Quest Secret: "))
account = server.load_account(SQKeypair.public_key)

resp = requests.get(f"https://horizon-testnet.stellar.org/accounts/{SQKeypair.public_key}").json()
signers = [_["key"] for _ in resp["signers"] if _["key"] != SQKeypair.public_key]

transaction = stellar_sdk.TransactionBuilder(source_account=account)

for signer in signers:
    transaction.append_set_options_op(
        signer=stellar_sdk.Signer.ed25519_public_key(signer, 0)
    )

if len(transaction.operations):
    transaction = transaction.build()
    transaction.sign(SQKeypair)

    resp = server.submit_transaction(transaction)
    print(resp)
else:
    print("No signers to remove")

print(f"https://stellar.expert/explorer/testnet/account/{SQKeypair.public_key}?filter=settings")
