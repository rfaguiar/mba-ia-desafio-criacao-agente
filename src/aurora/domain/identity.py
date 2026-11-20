from dataclasses import dataclass

from sqlalchemy import select

from aurora.domain.exceptions import SessionNotFoundError
from aurora.persistence.database import Database
from aurora.persistence.models import SessionRecord


@dataclass(frozen=True, slots=True)
class SessionIdentity:
    session_id: str
    apartment: str


async def resolve_identity(database: Database, session_id: str) -> SessionIdentity:
    async with database.session() as session:
        record = await session.get(SessionRecord, session_id)
    if record is None:
        raise SessionNotFoundError
    return SessionIdentity(session_id=session_id, apartment=record.apartment)


async def session_exists(database: Database, session_id: str) -> bool:
    async with database.session() as session:
        result = await session.scalar(
            select(SessionRecord.session_id).where(
                SessionRecord.session_id == session_id
            )
        )
        return result is not None

