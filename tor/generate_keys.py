from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519
import base64


def generate_tor_v3_keys():
    "Generates public, private keypair"
    private_key = x25519.X25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw	,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption())
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw)
    public = base64.b32encode(public_bytes).replace(b'=', b'') \
                       .decode("utf-8")
    private = base64.b32encode(private_bytes).replace(b'=', b'') \
                        .decode("utf-8")
    return public, private


if __name__ == '__main__':
    pub, priv = generate_tor_v3_keys()
    print(pub)
    print('\n')
    print(priv)
