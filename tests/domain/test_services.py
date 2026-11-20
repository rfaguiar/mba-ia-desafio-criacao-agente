from pathlib import Path

import pytest

from aurora.domain.exceptions import ReservationConflictError
from aurora.domain.identity import SessionIdentity
from aurora.domain.reservations import ReservationService
from aurora.domain.visitors import VisitorService
from aurora.persistence.bootstrap import restore_data
from aurora.persistence.database import Database
from aurora.persistence.models import SessionRecord


@pytest.fixture
async def services(tmp_path: Path):
    database = Database(f"sqlite+aiosqlite:///{tmp_path / 'domain.db'}")
    await database.create_schema()
    await restore_data(database, Path("dados"))
    async with database.session() as session:
        session.add(SessionRecord(session_id="session-101", apartment="101"))
    yield database, ReservationService(database), VisitorService(database)
    await database.close()


async def test_session_tools_only_return_own_data(services) -> None:
    _, reservations, visitors = services
    identity = SessionIdentity("session-101", "101")

    assert await reservations.list_own(identity) == [
        {"codigo": "RSV-1377", "area": "quadra", "data": "2030-03-09"}
    ]
    assert await visitors.list_own(identity) == []


async def test_availability_masks_other_resident(services) -> None:
    _, reservations, _ = services

    result = await reservations.availability("salao-de-festas", "2030-03-16")

    assert result == {
        "area": "salao-de-festas",
        "data": "2030-03-16",
        "livre": False,
    }
    assert "302" not in str(result)
    assert "RSV-4821" not in str(result)


async def test_cancel_only_affects_own_reservation(services) -> None:
    _, reservations, _ = services
    identity = SessionIdentity("session-101", "101")

    own = await reservations.cancel_own(identity, "quadra", "2030-03-09")
    other = await reservations.cancel_own(
        identity, "salao-de-festas", "2030-03-16"
    )

    assert own == {"cancelada": True, "area": "quadra", "data": "2030-03-09"}
    assert other == {
        "cancelada": False,
        "area": "salao-de-festas",
        "data": "2030-03-16",
    }


async def test_reservation_conflict_is_domain_error(services) -> None:
    _, reservations, _ = services
    identity = SessionIdentity("session-101", "101")

    with pytest.raises(ReservationConflictError):
        await reservations.create(identity, "salao-de-festas", "2030-03-16")


async def test_paid_and_free_area_confirmation_policy(services) -> None:
    _, reservations, _ = services

    assert await reservations.requires_confirmation("quadra", "2030-04-06") is False
    assert await reservations.requires_confirmation(
        "salao-de-festas", "2030-04-20"
    )

