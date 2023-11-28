from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from src.conf.config import settings

url = settings.sqlalchemy_database_url

engine = create_engine(url, echo=True, pool_size=5)

DBSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
