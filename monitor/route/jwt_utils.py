import base64
from datetime import timedelta, datetime, timezone

from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(
    email: str, expires_minutes, secret_key: str, algorithm: str = "RS512"
) -> str:
    expires_time = datetime.utcnow() + timedelta(expires_minutes)
    secret_key_bytes = base64.b64decode(secret_key)
    payload = {"exp": expires_time, "sub": email, "iat": datetime.now(tz=timezone.utc)}
    encoded_jwt = jwt.encode(payload, secret_key_bytes.decode("ascii"), algorithm)
    return encoded_jwt


def decode_access_token(access_token: str, public_key: str, algorithms):
    secret_key_bytes = base64.b64decode(public_key)
    options = {"require": ["exp, sub"]}
    decoded_token = jwt.decode(
        access_token, secret_key_bytes.decode("ascii"), algorithms, options=options
    )
    return decoded_token


def create_refresh_token(
    email: str, expires_minutes: int = 0, secret_key: bytes = None, algorithm: str = "RS512"
) -> str:
    expires_time = datetime.utcnow() + timedelta(expires_minutes)
    secret_key_str = secret_key.decode("utf-8")
    payload = {"exp": expires_time, "sub": email, "iat": datetime.now(tz=timezone.utc)}
    encoded_jwt = jwt.encode(payload, secret_key_str, algorithm)
    return encoded_jwt
