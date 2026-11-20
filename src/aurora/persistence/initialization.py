from sqlalchemy import func, select

from aurora.persistence.bootstrap import restore_data
from aurora.persistence.database import Database
from aurora.persistence.models import ApartmentRecord


async def initialize_database(database: Database, seed_directory) -> None:
    await database.create_schema()
    async with database.session() as session:
        apartment_count = await session.scalar(
            select(func.count()).select_from(ApartmentRecord)
        )
    if apartment_count == 0:
        await restore_data(database, seed_directory)

