import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request

SECRET_KEY = os.getenv("SECRET_KEY")  # type: ignore
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7


def create_token(user_id: str, avatar: str | None) -> str:
    payload = {
        "user_id": user_id,
        "avatar": avatar,
        "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_auth(request: Request) -> int:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(token)
    return int(payload["user_id"])
