# Environment Variables

This folder contains the environment variable files for the backend application.

## Required Files

These files must be created them when setting up the app. As they might contain sensitive data they are omited via `.gitignore` and are not saved in the repository.

### Global .env file

This file contains variables which will be loaded in every environment.

Filename: `.env`

```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Environment .env files

These files contain environment-specific variables. This will be loaded _after_ the global variables and will override any variables defined in the global file.

Filenames: `.env.development`, `.env.staging`, `.env.production`
```
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=
SECRET_KEY=
```

To create a new `SECRET_KEY` run the script:
```
python /scripts/generate_secret_key.py
```
