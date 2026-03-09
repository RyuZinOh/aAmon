from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Background, Chronux, UserBackground, Vault


async def buy_background(session: AsyncSession, user_id: int, bg_id: int) -> dict:
    bg = (
        await session.execute(select(Background).where(Background.bg_id == bg_id))
    ).scalar_one_or_none()
    if not bg:
        return {"ok": False, "error": "Background not found"}

    existing = (
        await session.execute(
            select(UserBackground).where(
                UserBackground.user_id == user_id,
                UserBackground.bg_id == bg_id,
            )
        )
    ).scalar_one_or_none()
    if existing:
        return {"ok": False, "error": "You already own this background"}

    chronux = (
        await session.execute(select(Chronux).where(Chronux.user_id == user_id))
    ).scalar_one_or_none()
    if not chronux or chronux.balance < bg.bg_cost:
        return {
            "ok": False,
            "error": f"Not enough Chronux. Need {bg.bg_cost}, have {chronux.balance if chronux else 0}",
        }

    chronux.balance -= bg.bg_cost

    user_bg = UserBackground(user_id=user_id, bg_id=bg_id, is_active=False)
    session.add(user_bg)
    await session.flush()

    vault = Vault(user_id=user_id, user_bg_id=user_bg.user_bg_id)
    session.add(vault)

    await session.commit()
    return {"ok": True, "message": f"Purchased {bg.bg_name} for {bg.bg_cost} Chronux"}
