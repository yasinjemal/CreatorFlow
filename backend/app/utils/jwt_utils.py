import time, jwt
from flask import current_app

def create_token(user_id: str, email: str, role: str = "user", exp_seconds: int = 60*60*24*7):
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": int(time.time()) + exp_seconds
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=["HS256"])
