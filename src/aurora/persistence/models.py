from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ApartmentRecord(Base):
    __tablename__ = "aurora_apartments"

    number: Mapped[str] = mapped_column(String(16), primary_key=True)
    resident: Mapped[str] = mapped_column(String(200), nullable=False)


class AreaRecord(Base):
    __tablename__ = "aurora_areas"

    area_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    fee: Mapped[float] = mapped_column(Float, nullable=False)


class SessionRecord(Base):
    __tablename__ = "aurora_sessions"

    session_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    apartment: Mapped[str] = mapped_column(
        ForeignKey("aurora_apartments.number"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class ReservationRecord(Base):
    __tablename__ = "aurora_reservations"
    __table_args__ = (
        Index(
            "uq_active_reservation_area_date",
            "area",
            "date",
            unique=True,
            sqlite_where=text("status = 'active'"),
        ),
        UniqueConstraint("code", name="uq_reservation_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        ForeignKey("aurora_reservation_codes.code"),
        nullable=False,
    )
    apartment: Mapped[str] = mapped_column(
        ForeignKey("aurora_apartments.number"),
        nullable=False,
    )
    area: Mapped[str] = mapped_column(
        ForeignKey("aurora_areas.area_id"),
        nullable=False,
    )
    date: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class ReservationCodeRecord(Base):
    __tablename__ = "aurora_reservation_codes"

    code: Mapped[str] = mapped_column(String(80), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class VisitorRecord(Base):
    __tablename__ = "aurora_visitors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    apartment: Mapped[str] = mapped_column(
        ForeignKey("aurora_apartments.number"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class ConfirmationRecord(Base):
    __tablename__ = "aurora_confirmations"

    confirmation_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        ForeignKey("aurora_sessions.session_id"),
        nullable=False,
    )
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    requesting_agent: Mapped[str] = mapped_column(String(100), nullable=False)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

