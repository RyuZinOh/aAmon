from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Hero(Base):
    __tablename__ = "heroes"
    hero_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hero_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hero_image: Mapped[str] = mapped_column(Text, nullable=False)
    hero_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    hero_lore: Mapped[str | None] = mapped_column(Text, nullable=True)

    hero_attack: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_specialattack: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_defence: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_specialdefence: Mapped[int] = mapped_column(Integer, nullable=False)
    hero_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)

    user_heroes: Mapped[list["UserHero"]] = relationship(  # type: ignore
        "UserHero", back_populates="hero"
    )
