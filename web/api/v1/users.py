from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import SessionLocal
from services.user_service import get_user
from web.utils.jwt import require_auth

router = APIRouter()


async def get_session():
    async with SessionLocal() as session:
        yield session


@router.get("/users/me")
async def me(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(require_auth),
):
    user = await get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not registered in bot")

    token_payload = require_auth(request)
    avatar_hash = None
    token = request.cookies.get("token")
    if token:
        from web.utils.jwt import decode_token

        payload = decode_token(token)
        avatar_hash = payload.get("avatar")

    avatar_url = (
        f"https://cdn.discordapp.com/avatars/{user.uid}/{avatar_hash}.png"
        if avatar_hash
        else f"https://cdn.discordapp.com/embed/avatars/{int(user.uid) % 5}.png"
    )

    return {
        "uid": user.uid,
        "username": user.username,
        "bio": user.bio,
        "registered_at": user.registered_at,
        "chronux_balance": user.chronux.balance if user.chronux else 0,
        "avatar_url": avatar_url,
    }
