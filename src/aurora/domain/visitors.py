from sqlalchemy import select

from aurora.domain.identity import SessionIdentity
from aurora.domain.validation import validate_date, validate_visitor_name
from aurora.persistence.database import Database
from aurora.persistence.models import VisitorRecord


class VisitorService:
    def __init__(self, database: Database) -> None:
        self.database = database

    async def list_own(self, identity: SessionIdentity) -> list[dict[str, str]]:
        return await self.list_apartment(identity.apartment)

    async def list_apartment(self, apartment: str) -> list[dict[str, str]]:
        async with self.database.session() as session:
            records = (
                await session.scalars(
                    select(VisitorRecord)
                    .where(VisitorRecord.apartment == apartment)
                    .order_by(VisitorRecord.date, VisitorRecord.name)
                )
            ).all()
        return [{"nome": record.name, "data": record.date} for record in records]

    async def authorize(
        self,
        identity: SessionIdentity,
        raw_name: str,
        raw_date: str,
    ) -> dict[str, str]:
        name = validate_visitor_name(raw_name)
        date = validate_date(raw_date)
        async with self.database.session() as session:
            session.add(
                VisitorRecord(
                    apartment=identity.apartment,
                    name=name,
                    date=date,
                )
            )
        return {"nome": name, "data": date}

