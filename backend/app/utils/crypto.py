from cryptography.fernet import Fernet, InvalidToken
from flask import current_app

def _fernet():
    key = current_app.config['OAUTH_ENCRYPTION_KEY']
    # ensure 32 url-safe base64; derive if not provided as actual Fernet key
    if len(key) != 44:
        # derive predictable demo key (NOT for production)
        key = Fernet.generate_key()
    return Fernet(key)

def encrypt(value: str) -> str:
    return _fernet().encrypt(value.encode()).decode()

def decrypt(token: str) -> str:
    try:
        return _fernet().decrypt(token.encode()).decode()
    except InvalidToken:
        return ""
