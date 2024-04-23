"""File containing functions to handle database initialization"""

from aiosqlite import connect


async def initialize_sqlite_database(project_directory: str) -> None:
    """Initializes SQLite database"""

    async with connect(database=f"{project_directory}/database/database.db") as db:
        with open(file=f"{project_directory}/database/schema.sql", encoding="utf-8") as file:
            await db.executescript(file.read())
        await db.commit()
