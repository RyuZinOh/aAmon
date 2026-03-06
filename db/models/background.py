from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Background(Base):
    __tablename__ = "backgrounds"

    bg_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bg_url: Mapped[str] = mapped_column(Text, nullable=False)
    bg_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bg_lore: Mapped[str | None] = mapped_column(Text, nullable=True)
    bg_rarity: Mapped[str] = mapped_column(String(20), nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)

    user_backgrounds: Mapped[list["UserBackground"]] = relationship(  # type: ignore
        "UserBackground", back_populates="background"
    )
