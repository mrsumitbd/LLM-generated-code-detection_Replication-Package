from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

def verify_credentials(public_key_bytes):
                public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
                try:
                    public_key.verify(signature, message.encode("utf-8"))
                except InvalidSignature:
                    raise Exception("Invalid signature")