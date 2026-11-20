import asyncio

from aurora.config import settings
from aurora.persistence.bootstrap import restore_data
from aurora.persistence.database import Database


async def main() -> None:
    database = Database(settings.database_url)
    try:
        await database.create_schema()
        await restore_data(database, settings.seed_directory)
        print(f"Dados restaurados em {settings.database_url}")
    finally:
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())

