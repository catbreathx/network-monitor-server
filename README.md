# Network Monitor

## Database

To (re-)create a local database, run the `initialize.sh` script:

```
sh initialize_db.sh
```


### Alembic

Database changes are managed using Alembic.

### Run Migrations

To apply all alembic migrations, run:

```
alembic upgrade head
```

Or, to apply up to a specific revision

```
alembic upgrade <revision id>
```

### Create a new Migration

To create a new revision:

```
alembic revision
```

To automatically generate changes, use the `--autogenerate` option,

i.e.,

```
alembic revision --autogenerate
```
