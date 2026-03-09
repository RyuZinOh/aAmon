from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class UserBackground(Base):
    __tablename__ = "user_backgrounds"

    user_bg_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False
    )
    bg_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("backgrounds.bg_id", ondelete="CASCADE"), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    acquired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="backgrounds")  # type: ignore
    background: Mapped["Background"] = relationship(  # type: ignore
        "Background", back_populates="user_backgrounds"
    )
    vault: Mapped["Vault"] = relationship(  # type: ignore
        "Vault", back_populates="user_background", uselist=False
    )
