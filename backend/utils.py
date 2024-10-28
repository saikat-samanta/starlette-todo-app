import hashlib
import jwt

import settings

salt = str(settings.SALT)
secret = str(settings.SECRET)


def hash_password(password):
    return hashlib.sha256((password + salt).encode()).hexdigest()


def check_password(password, hashed):
    return hashlib.sha256((password + salt).encode()).hexdigest() == hashed


def jwt_encode(payload):
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def jwt_decode(token):
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    return payload
