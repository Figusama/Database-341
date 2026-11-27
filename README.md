Hello


## Software Version

- Python dependencies are pinned in `requirements.txt`,
- The frontend declares React and React DOM, Vite , and @vitejs/plugin-react. Use `frontend/package-lock.json` for the resolved frontend dependency versions.
- Database: PostgreSQL (Supabase)

## Configuration and secrets

The application reads `DATABASE_URL` from the root `.env` file. For Supabase URLs, the database helper requires SSL. It prefers psycopg2 when installed, otherwise it tries pg8000. `SQL_ECHO` controls SQLAlchemy SQL logging and defaults to true.

Create a local `.env` with your own database connection string; do not commit credentials. The included `.env` contains credentials and should be treated as private. If those credentials have been shared unintentionally, rotate them with the database provider.

in `.env` include DATABASE_URL
`DATABASE_URL=secret_url`

Checks declared in the database schema/models include:

- Required columns are NOT NULL, subject to explicitly optional fields such as ORCID, session assignment, change note, and confidential review comments.
- User email is unique.
- Conference end date cannot precede its start date.
- Session end time must be later than start time.
- Reviewer experience cannot be negative.
- Paper status is one of `submitted`, `under review`, `accepted`, `rejected`, or `withdrawn`.
- Author position and paper version number must be positive; author positions must be unique within a paper.
- Review scores are 1–5, recommendations are `accept` or `reject`, and a reviewer can submit at most one review per paper.
- The Part 1 SQL schema defines a partial unique index allowing at most one corresponding author per paper.

## Explaining files
`seed.sql` - our seed/data used on Part 1.

`schema.sql` - schema (tables) for our Part 1.

`create_tables.py` - table creation for Part 2 (uses models that are in `/backend/conference`, `/backend/paper`, `/backend/track`, `/backend/user`)

`remove_tables.py` - table removal for Part 2

If there are some troubles or you want to go back you can `remove_tables.py` and then `create_tables.py`.

Every code for Task 2 are in `/task2`

Explaining everything in `/task2`
- `populating.py` - populates the database with the data inside `data.py` (data.py is the same data as the seed.sql) (Task 2, 2)
- `updating.py` - updates some data that are specified in (Task 2, 3)
- `deleting.py` - deletes some data that are specified in (Task 2, 4)
- `simple_queries.py` - runs the simple queries that are specified in (Task 2, 5)
- `complex_queries.py` - runs the conplex queries that are specified in (Task 2, 6)
- `derived_attr.py` - runs the query with a derived attribute that is specified in (Task 2, 7)
- `view.py` - runs the view operation that is specified in (Task 2, 8)

## Running the course queries

The task scripts use the Part 2 SQLModel schema and configured database. From the project root, activate the virtual environment if available and install dependencies if needed:
```
python -m venv venv
```

```
source venv/bin/activate
pip install -r requirements.txt
```


```
PYTHONPATH=. python task2/simple_queries.py
PYTHONPATH=. python task2/complex_queries.py
PYTHONPATH=. python task2/derived_attr.py
PYTHONPATH=. python task2/view.py
PYTHONPATH=. python task2/populating.py
PYTHONPATH=. python task2/updating.py
PYTHONPATH=. python task2/deleting.py
```


Task 3 backend part is in `/backend` where each subdirectory has routers, models, schemas.
`router.py`'s include general functions
`schemas.py`'s include I/O to/from the database
`models`'s include general tables of the schema.
