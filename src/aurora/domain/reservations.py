import unicodedata
from datetime import UTC, datetime
from secrets import token_hex

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from aurora.domain.exceptions import ReservationConflictError, ValidationError
from aurora.domain.identity import SessionIdentity
from aurora.domain.validation import validate_date
from aurora.persistence.database import Database
from aurora.persistence.models import (
    AreaRecord,
    ReservationCodeRecord,
    ReservationRecord,
)


class ReservationService:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def area(self, area: str) -> AreaRecord:
        normalized = self._normalize_area(area)
        async with self.database.session() as session:
            record = await session.get(AreaRecord, normalized)
            if record is None:
                records = (await session.scalars(select(AreaRecord))).all()
                record = next(
                    (
                        candidate
                        for candidate in records
                        if self._normalize_area(candidate.name) == normalized
                    ),
                    None,
                )
        if record is None:
            raise ValidationError("Área comum não encontrada.")
        return record

    async def list_own(self, identity: SessionIdentity) -> list[dict[str, str]]:
        return await self.list_apartment(identity.apartment)

    async def list_apartment(self, apartment: str) -> list[dict[str, str]]:
        async with self.database.session() as session:
            records = (
                await session.scalars(
                    select(ReservationRecord)
                    .where(
                        ReservationRecord.apartment == apartment,
                        ReservationRecord.status == "active",
                    )
                    .order_by(ReservationRecord.date, ReservationRecord.area)
                )
            ).all()
        return [
            {"codigo": record.code, "area": record.area, "data": record.date}
            for record in records
        ]

    async def availability(self, area: str, raw_date: str) -> dict[str, object]:
        value = validate_date(raw_date)
        canonical_area = (await self.area(area)).area_id
        async with self.database.session() as session:
            record = await session.scalar(
                select(ReservationRecord.id).where(
                    ReservationRecord.area == canonical_area,
                    ReservationRecord.date == value,
                    ReservationRecord.status == "active",
                )
            )
        return {"area": canonical_area, "data": value, "livre": record is None}

    async def requires_confirmation(self, area: str, raw_date: str) -> bool:
        validate_date(raw_date)
        return (await self.area(area)).fee > 0

    async def create(
        self,
        identity: SessionIdentity,
        area: str,
        raw_date: str,
    ) -> dict[str, str]:
        value = validate_date(raw_date)
        canonical_area = (await self.area(area)).area_id

        for _ in range(3):
            code = f"RSV-{token_hex(6).upper()}"
            try:
                async with self.database.session() as session:
                    session.add(ReservationCodeRecord(code=code))
                    await session.flush()
                    session.add(
                        ReservationRecord(
                            code=code,
                            apartment=identity.apartment,
                            area=canonical_area,
                            date=value,
                        )
                    )
                    await session.flush()
                return {"codigo": code, "area": area, "data": value}
            except IntegrityError as error:
                if await self._is_occupied(canonical_area, value):
                    raise ReservationConflictError from error
        raise ValidationError("Não foi possível gerar um código de reserva único.")

    async def cancel_own(
        self,
        identity: SessionIdentity,
        area: str,
        raw_date: str,
    ) -> dict[str, object]:
        value = validate_date(raw_date)
        canonical_area = (await self.area(area)).area_id
        async with self.database.session() as session:
            record = await session.scalar(
                select(ReservationRecord).where(
                    ReservationRecord.apartment == identity.apartment,
                    ReservationRecord.area == canonical_area,
                    ReservationRecord.date == value,
                    ReservationRecord.status == "active",
                )
            )
            if record is None:
                return {
                    "cancelada": False,
                    "area": canonical_area,
                    "data": value,
                }
            record.status = "cancelled"
            record.cancelled_at = datetime.now(UTC)
        return {"cancelada": True, "area": canonical_area, "data": value}

    async def _is_occupied(self, area: str, date: str) -> bool:
        async with self.database.session() as session:
            result = await session.scalar(
                select(ReservationRecord.id).where(
                    ReservationRecord.area == area,
                    ReservationRecord.date == date,
                    ReservationRecord.status == "active",
                )
            )
        return result is not None

    @staticmethod
    def _normalize_area(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value)
        ascii_value = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )
        return "-".join(ascii_value.lower().strip().split())

