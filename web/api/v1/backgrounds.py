from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import SessionLocal
from web.services.background_service import fetch_all_backgrounds, fetch_background
from web.services.buy_service import buy_background
from web.utils.jwt import require_auth

router = APIRouter()


async def get_session():
    async with SessionLocal() as session:
        yield session


@router.get("/backgrounds")
async def list_backgrounds(session: AsyncSession = Depends(get_session)):
    return await fetch_all_backgrounds(session)


@router.get("/backgrounds/{bg_id}")
async def get_background(bg_id: int, session: AsyncSession = Depends(get_session)):
    bg = await fetch_background(session, bg_id)
    if not bg:
        raise HTTPException(status_code=404, detail="Background not found")
    return bg


@router.post("/backgrounds/{bg_id}/buy")
async def buy_bg(
    bg_id: int,
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(require_auth),
):
    result = await buy_background(session, user_id, bg_id)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
