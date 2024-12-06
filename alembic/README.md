# Database Migration Guide

Use Alembic for managing database migrations.

## Creating Database Migrations

### Quick Start

For quicker development migrations, use the helper scripts:

```sh
# Generate a new migration
./scripts/migrate "migration message"

# Apply migrations to development database
./scripts/dev_migrate
```

### New Migration Protocol

When creating a new migration, follow these steps:

1. **Generate a Migration Revision**

    ```sh
    alembic revision --autogenerate -m "Description of changes"
    ```

    - Choose a descriptive message that clearly indicates the changes
    - Use proper sentence punctuation, but do not add a period

2. **Review Generated Migration**

    - Location: `./alembic/versions/<hash>_description.py`
    - Verify the auto-generated changes
    - Common areas to check:
        - Column modifications
        - Foreign key relationships
        - Index creation/removal
        - Custom data types
    - Add any necessary imports or manual adjustments

3. **Version Control**

    ```sh
    git add ./alembic/versions/<migration_file>.py
    git commit -m "Migration: Description of changes"
    ```

    - Always prefix migration commit messages with "Migration:"
    - Keep the commit message consistent with the migration description

4. **Apply Migration**

    ```sh
    ENVIRONMENT=development alembic upgrade head
    ```

    - Substitute `development` with the intended database environment

## Best Practices
- Create atomic migrations (one change per migration)
- Always review auto-generated code before committing
- Test migrations on development before applying to production
- Include both `upgrade()` and `downgrade()` operations
- Back up production database before applying migrations

## Troubleshooting

If you encounter migration conflicts:

1. Run `alembic history` to view the migration chain
2. Use `alembic current` to check current database version
3. For emergency rollback: `alembic downgrade -1`

## Table Metadata Fields

The following fields are transparently added to all tables during migrations—no additional configuration is needed:

| Field       | Deafult | Description |
|-------------|----------|-------|
| `is_active` | True   | Soft delete flag |
| `is_flagged`| False  | General flag |
| `notes`     | None   | General notes field |
| `created_at`| UTC    | Timestamp of row creation |
| `updated_at`| UTC    | Timestamp of last row update |

These fields are defined as part of the base models which get inherited by database table definitions.

Location in the code:

- `Base` in `./app/db/base.py`
- `BaseModel` in `./app/schemas/base.py`

### Handling Update Timestamps

When creating tables, the migration system will automatically:

- Create a PostgreSQL function `set_updated_at()` if it doesn't exist
- Add a `BEFORE UPDATE` trigger on affected tables
- Automatically update the `updated_at` column with the current UTC timestamp whenever a row is updated

This happens transparently during migrations—no additional configuration is needed.

Example:
```python
# Database model
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

The migration will automatically handle:

- Column creation: append metadata fields
- Function creation: `set_updated_at()`
- Trigger creation: `update_timestamp` on the `users` table
- UTC timestamp updates: Handled at database level

### Switching Database Engines

Ensure the following steps are taken to match the new database engine:

- In the `./app/envs/.env` file:
    - Update the variable: `DATABASE_TIMESTAMP_UTC`

- In the `./alembic/env.py` file:
    - Update the function: `set_updated_at()`
    - Update the trigger: `update_timestamp`

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Legal

Private and Confidential. All rights reserved.
