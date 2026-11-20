import json
from pathlib import Path
from typing import Any

from sqlalchemy import delete

from aurora.persistence.database import Database
from aurora.persistence.models import (
    ApartmentRecord,
    AreaRecord,
    ConfirmationRecord,
    ReservationCodeRecord,
    ReservationRecord,
    VisitorRecord,
)


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


async def restore_data(database: Database, seed_directory: Path) -> None:
    apartments = _load(seed_directory / "apartamentos.json")
    areas = _load(seed_directory / "areas.json")
    reservations = _load(seed_directory / "reservas.json")
    visitors = _load(seed_directory / "visitantes.json")

    async with database.session() as session:
        await session.execute(delete(ConfirmationRecord))
        await session.execute(delete(ReservationRecord))
        await session.execute(delete(ReservationCodeRecord))
        await session.execute(delete(VisitorRecord))
        for item in apartments:
            await session.merge(
                ApartmentRecord(number=item["numero"], resident=item["morador"])
            )
        for item in areas:
            await session.merge(
                AreaRecord(
                    area_id=item["id"],
                    name=item["nome"],
                    fee=float(item["taxa"]),
                )
            )
        await session.flush()
        session.add_all(ReservationCodeRecord(code=item["codigo"]) for item in reservations)
        await session.flush()
        session.add_all(
            ReservationRecord(
                code=item["codigo"],
                apartment=item["apartamento"],
                area=item["area"],
                date=item["data"],
            )
            for item in reservations
        )
        session.add_all(
            VisitorRecord(
                apartment=item["apartamento"],
                name=item["nome"],
                date=item["data"],
            )
            for item in visitors
        )

