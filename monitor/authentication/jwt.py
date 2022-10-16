import base64
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from monitor.database.models import User
from monitor.exceptions.exceptions import AuthenticationException
from monitor.schema.jwt import JwtUser

ALGORITHM = "RS512"
ONE_WEEK = 24 * 60 * 7


def create_jwt_token(
    user: User, expiration_minutes: int, secret_key: str, algorithm=ALGORITHM
) -> str:
    now = datetime.utcnow()
    expire_datetime = datetime.utcnow() + timedelta(minutes=expiration_minutes)

    payload = {
        "id": user.id,
        "email": user.email,
        "exp": expire_datetime,
        "sub": str(user.id),
        "nbf": now,
        "iat": now,
    }

    secret_key_bytes = base64.b64decode(secret_key)
    encoded_jwt = jwt.encode(
        claims=payload, key=secret_key_bytes.decode("ascii"), algorithm=algorithm
    )

    return encoded_jwt


def get_user_from_jwt_token(
    jwt_token: str, public_key: str, algorithms: str | list = None
) -> JwtUser:
    if algorithms is None:
        algorithms = [ALGORITHM]

    try:
        public_key_bytes = base64.b64decode(public_key)
        payload = jwt.decode(jwt_token, public_key_bytes.decode("ascii"), algorithms=algorithms)
        user = JwtUser(id=payload["id"], email=payload["email"])

    except JWTError as e:
        raise AuthenticationException(e)

    return user


def create_refresh_token(
    email: str, expires_minutes: int = ONE_WEEK, secret_key: str = None, algorithm: str = ALGORITHM
) -> str:
    expires_time = datetime.utcnow() + timedelta(expires_minutes)
    secret_key_bytes = base64.b64decode(secret_key)
    payload = {"exp": expires_time, "sub": email, "iat": datetime.now(tz=timezone.utc)}
    encoded_jwt = jwt.encode(payload, secret_key_bytes.decode("ascii"), algorithm)
    return encoded_jwt
