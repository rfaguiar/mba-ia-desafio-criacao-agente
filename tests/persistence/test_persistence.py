from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from aurora.persistence.bootstrap import restore_data
from aurora.persistence.database import Database
from aurora.persistence.models import (
    ReservationCodeRecord,
    ReservationRecord,
    VisitorRecord,
)


@pytest.fixture
async def database(tmp_path: Path):
    instance = Database(f"sqlite+aiosqlite:///{tmp_path / 'aurora.db'}")
    await instance.create_schema()
    await restore_data(instance, Path("dados"))
    yield instance
    await instance.close()


async def test_restore_loads_initial_data_and_is_repeatable(database: Database) -> None:
    await restore_data(database, Path("dados"))

    async with database.session() as session:
        reservations = (await session.scalars(select(ReservationRecord))).all()
        visitors = (await session.scalars(select(VisitorRecord))).all()

    assert {item.code for item in reservations} == {
        "RSV-1377",
        "RSV-4821",
        "RSV-2950",
    }
    assert {(item.name, item.date) for item in visitors} == {
        ("Marina Duarte", "2030-03-16"),
        ("Paulo Nogueira", "2030-03-23"),
    }


async def test_reservation_area_and_date_are_unique_while_active(database: Database) -> None:
    with pytest.raises(IntegrityError):
        async with database.session() as session:
            session.add(ReservationCodeRecord(code="RSV-DUPLICATE"))
            await session.flush()
            session.add(
                ReservationRecord(
                    code="RSV-DUPLICATE",
                    apartment="101",
                    area="salao-de-festas",
                    date="2030-03-16",
                )
            )
            await session.flush()


async def test_cancelled_code_stays_reserved_and_slot_can_be_reused(
    database: Database,
) -> None:
    async with database.session() as session:
        reservation = await session.scalar(
            select(ReservationRecord).where(ReservationRecord.code == "RSV-1377")
        )
        assert reservation is not None
        reservation.status = "cancelled"
    async with database.session() as session:
        session.add(ReservationCodeRecord(code="RSV-NEW"))
        await session.flush()
        session.add(
            ReservationRecord(
                code="RSV-NEW",
                apartment="201",
                area="quadra",
                date="2030-03-09",
            )
        )
    async with database.session() as session:
        count = await session.scalar(
            select(func.count()).select_from(ReservationCodeRecord)
        )
        assert count == 4
