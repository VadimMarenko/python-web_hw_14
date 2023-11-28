# Implementation of the FastAPI project

The `/.env` file with environment variables is required for the project to work.
Create it with this content and substitute your values.

```/.env
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DOMAIN=
POSTGRES_PORT=

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DOMAIN}:${POSTGRES_PORT}/${POSTGRES_DB}

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=

SECRET_KEY=
ALGORITHM=

REDIS_HOST=
REDIS_PORT=

CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Launching the application

```
docker-compose up -d
alembic upgrade head
uvicorn main:app --reload
