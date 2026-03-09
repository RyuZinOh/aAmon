from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Background


def bg_to_dict(bg: Background) -> dict:
    return {
        "id": bg.bg_id,
        "name": bg.bg_name,
        "lore": bg.bg_lore,
        "rarity": bg.bg_rarity,
        "cost": bg.bg_cost,
        "url": f"/public/backgrounds/{bg.bg_url}",
    }


async def fetch_all_backgrounds(session: AsyncSession) -> list[dict]:
    result = await session.execute(select(Background).order_by(Background.bg_cost))
    return [bg_to_dict(bg) for bg in result.scalars().all()]


async def fetch_background(session: AsyncSession, bg_id: int) -> dict | None:
    result = await session.execute(select(Background).where(Background.bg_id == bg_id))
    bg = result.scalar_one_or_none()
    return bg_to_dict(bg) if bg else None
