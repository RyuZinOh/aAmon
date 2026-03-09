from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class UserHero(Base):
    __tablename__ = "user_heroes"

    user_hero_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False
    )
    hero_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("heroes.hero_id", ondelete="CASCADE"), nullable=False
    )

    hero_attack: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_specialattack: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_defence: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_specialdefence: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_speed: Mapped[int] = mapped_column(Integer, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    acquired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="heroes")  # type: ignore
    hero: Mapped["Hero"] = relationship("Hero", back_populates="user_heroes")  # type: ignore
    vault: Mapped["Vault"] = relationship(  # type: ignore
        "Vault", back_populates="user_hero", uselist=False
    )
