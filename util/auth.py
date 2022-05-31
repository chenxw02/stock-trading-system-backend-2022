import jwt
from config import jwt_secret_key
from error.invalid_jwt import InvalidJWT


def decode_token(token):
    try:
        info = jwt.decode(token, jwt_secret_key, algorithms="HS256")
    except Exception:
        raise InvalidJWT
    return info
