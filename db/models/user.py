from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class User(Base):
    __tablename__ = "users"
    uid: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    heroes: Mapped[list["UserHero"]] = relationship(  # type: ignore
        "UserHero", back_populates="user", cascade="all, delete-orphan"
    )
    backgrounds: Mapped[list["UserBackground"]] = relationship(  # type: ignore
        "UserBackground", back_populates="user", cascade="all, delete-orphan"
    )
    vault: Mapped[list["Vault"]] = relationship(  # type: ignore
        "Vault", back_populates="user", cascade="all, delete-orphan"
    )
