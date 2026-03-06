from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def get_user(session: AsyncSession, discord_id: int) -> User | None:
    result = await session.execute(select(User).where(User.uid == discord_id))
    return result.scalar_one_or_none()


async def register_user(
    session: AsyncSession, discord_id: int, username: str
) -> tuple[User, bool]:
    existing = await get_user(session, discord_id)
    if existing:
        return existing, False

    user = User(uid=discord_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user, True
