# Bibliotecas Externas
from pysequoia import Cert, encrypt

ENCODING = 'utf-8'

def encrypt_session_key(pubkey_armored: str, session_key: bytes) -> str:
    recipient = Cert.from_bytes(pubkey_armored.encode(ENCODING))
    encrypted = encrypt(recipients=[recipient], bytes=session_key)
    return encrypted.decode(ENCODING)

