import os
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from web.utils.jwt import TOKEN_EXPIRE_DAYS, create_token, decode_token

router = APIRouter()


@router.get("/login")
async def login():
    params = urlencode(
        {
            "client_id": os.getenv("DISCORD_CLIENT_ID"),
            "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
            "response_type": "code",
            "scope": "identify",
        }
    )
    return RedirectResponse(f"https://discord.com/oauth2/authorize?{params}")


@router.get("/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": os.getenv("DISCORD_CLIENT_ID"),
                "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_resp.json()

        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail=f"Discord error: {token_data}")

        user_resp = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user = user_resp.json()

    jwt_token = create_token(str(user["id"]), user.get("avatar"))

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="token",
        value=jwt_token,
        httponly=True,
        max_age=TOKEN_EXPIRE_DAYS * 86400,
        samesite="lax",
    )
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("token")
    return response


@router.get("/me")
async def me(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(token)
    return {
        "authenticated": True,
        "user_id": payload["user_id"],
        "avatar": payload.get("avatar"),
    }
