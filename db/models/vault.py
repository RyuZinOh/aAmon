from sqlalchemy import BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Vault(Base):
    __tablename__ = "vault"

    vauld_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False
    )
    user_hero_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("user_heroes.user_hero_id", ondelete="CASCADE"),
        nullable=True,
    )
    user_bg_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("user_backgrounds.user_bg_id", ondelete="CASCADE"),
        nullable=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="vault")  # type:ignore
    user_hero: Mapped["UserHero | None"] = relationship(  # type: ignore
        "UserHero", back_populates="vault"
    )
    user_background: Mapped["UserBackground | None"] = relationship(  # type: ignore
        "UserBackground", back_populates="vault"
    )
