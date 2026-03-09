from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Chronux(Base):
    __tablename__ = "choronux"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.uid", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="chronux")  # type: ignore
