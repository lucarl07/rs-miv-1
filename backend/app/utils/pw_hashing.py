# Bibliotecas Externas
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# Hashing de senha 
pwd_context = PasswordHash([BcryptHasher()])

def hash_password(plain_password: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

