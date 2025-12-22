import hashlib
import ecdsa

def verify_credentials(public_key_bytes):
    try:
        # Load the public key from the provided bytes
        vk = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.NIST256p)

        # Read the user's input for the message and signature
        message = input("Enter the message: ").encode()
        signature_bytes = bytes.fromhex(input("Enter the signature: "))

        # Verify the signature
        if vk.verify(signature_bytes, message):
            return True
        else:
            return False
    except (ValueError, ecdsa.BadSignatureError):
        return False