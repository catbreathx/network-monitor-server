# Network Monitor

## Create Virtual Environment

To create a virtual environment:
poetry env use <python executable>

For example:
```
poetry env use python3.10
```

To activate:

```
poetry shell
```

To install packages, use the `install` command:

```
poetry install
```

## Database

To (re-)create a local database, run the `initialize.sh` script:

```
sh initialize_db.sh
```

create e2e database:

```
sh initialize_e2e_db.sh
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
