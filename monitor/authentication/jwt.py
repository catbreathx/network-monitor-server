from datetime import datetime, timedelta

from jose import jwt, JWTError

from monitor.database.models import User
from monitor.exceptions.exceptions import AuthenticationException
from monitor.schema.jwt import JwtUser

ALGORITHM = "HS512"


def create_jwt_token(
    user: User, expiration_minutes: int, secret_key: str, algorithm=ALGORITHM
) -> str:
    now = datetime.utcnow()
    expire_datetime = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    payload = {"id": user.id, "email": user.email}

    payload.update({"exp": expire_datetime, "sub": str(user.id), "nbf": now})
    encoded_jwt = jwt.encode(claims=payload, key=secret_key, algorithm=algorithm)

    return encoded_jwt


def decode_jwt_token(jwt_token: str, secret_key: str, algorithms=None) -> JwtUser:
    if algorithms is None:
        algorithms = [ALGORITHM]

    try:
        payload = jwt.decode(jwt_token, secret_key, algorithms=algorithms)
        user = JwtUser(id=payload["id"], email=payload["email"])

    except JWTError as e:
        raise AuthenticationException(e)

    return user
