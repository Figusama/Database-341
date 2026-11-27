Hello


`seed.sql` - our seed/data used on Part 1.

`schema.sql` - schema (tables) for our Part 1.

`create_tables` - table creation for Part 2 (uses models that are in `/backend/conference`, `/backend/paper`, `/backend/track`, `/backend/user`)

`remove_tables` - table removal for Part 2

If there are some troubles or you want to go back you can `remove_tables` and then `create_tables`.

Every code for Task 2 are in `/task2`

Explaining everything in `/task2`
- `populating.py` - populates the database with the data inside `data.py` (data.py is the same data as the seed.sql) (Task 2, 2)
- `updating.py` - updates some data that are specified in (Task 2, 3)
- `deleting.py` - deletes some data that are specified in (Task 2, 4)
- `simple_queries.py` - runs the simple queries that are specified in (Task 2, 5)
- `complex_queries.py` - runs the conplex queries that are specified in (Task 2, 6)
- `derived_attr.py` - runs the query with a derived attribute that is specified in (Task 2, 7)
- `view.py` - runs the view operation that is specified in (Task 2, 8)

To run them use:
- For Mac `PYTHONPATH=. python task2/(python file name)`
    Example:
    `PYTHONPATH=. python task2/populating.py`

The website for Task 3 is https://database-341.onrender.com

Task 3 backend part is in `/backend` where each subdirectory has routers, models, schemas.
`router.py`'s include general functions
`schemas.py`'s include I/O to/from the database
`models`'s include general tables of the schema.
