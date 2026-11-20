from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select, update

from aurora.persistence.database import Database
from aurora.persistence.models import ConfirmationRecord


@dataclass(frozen=True, slots=True)
class PendingConfirmation:
    confirmation_id: str
    action: str
    details: dict[str, str]
    invocation_id: str
    requesting_agent: str


class ConfirmationMirror:
    """Espelha as confirmações nativas do ADK para o contrato HTTP."""

    def __init__(self, database: Database) -> None:
        self.database = database

    async def upsert_pending(
        self,
        *,
        confirmation_id: str,
        session_id: str,
        action: str,
        details: dict[str, str],
        payload: dict[str, object],
        invocation_id: str,
        requesting_agent: str,
    ) -> None:
        async with self.database.session() as session:
            existing = await session.get(ConfirmationRecord, confirmation_id)
            if existing is None:
                session.add(
                    ConfirmationRecord(
                        confirmation_id=confirmation_id,
                        session_id=session_id,
                        action=action,
                        details=details,
                        payload={**payload, "invocation_id": invocation_id},
                        requesting_agent=requesting_agent,
                        status="pending",
                    )
                )

    async def list_pending(self, session_id: str) -> list[dict[str, object]]:
        async with self.database.session() as session:
            records = (
                await session.scalars(
                    select(ConfirmationRecord)
                    .where(
                        ConfirmationRecord.session_id == session_id,
                        ConfirmationRecord.status == "pending",
                    )
                    .order_by(ConfirmationRecord.created_at)
                )
            ).all()
        return [
            {
                "id": record.confirmation_id,
                "acao": record.action,
                "detalhes": record.details,
            }
            for record in records
        ]

    async def get_pending(
        self,
        session_id: str,
        confirmation_id: str,
    ) -> PendingConfirmation | None:
        async with self.database.session() as session:
            record = await session.scalar(
                select(ConfirmationRecord).where(
                    ConfirmationRecord.session_id == session_id,
                    ConfirmationRecord.confirmation_id == confirmation_id,
                    ConfirmationRecord.status == "pending",
                )
            )
        if record is None:
            return None
        return PendingConfirmation(
            confirmation_id=record.confirmation_id,
            action=record.action,
            details=dict(record.details),
            invocation_id=str(record.payload["invocation_id"]),
            requesting_agent=record.requesting_agent,
        )

    async def resolve(
        self,
        confirmation_id: str,
        session_id: str,
        status: str,
        result: str,
    ) -> bool:
        async with self.database.session() as session:
            db_result = await session.execute(
                update(ConfirmationRecord)
                .where(
                    ConfirmationRecord.confirmation_id == confirmation_id,
                    ConfirmationRecord.session_id == session_id,
                    ConfirmationRecord.status == "pending",
                )
                .values(
                    status=status,
                    result=result,
                    resolved_at=datetime.now(UTC),
                )
            )
        return db_result.rowcount == 1

