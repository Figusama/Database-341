from sqlalchemy import text, MetaData
from database.database import engine
existing = MetaData()
existing.reflect(engine)

with engine.begin() as conn:
    for table in existing.sorted_tables:
        conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE') )