from typing import Generator
from sqlalchemy import (
    inspect,
    create_engine,
)
from sqlalchemy.dialects.postgresql.base import PGInspector
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

import config as config
from core.utils.log_config import log


class connect:
    DATABASE_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"


connect = connect()

# Session
connection_url = connect.DATABASE_URL
log.warn(f"Db Connection Url --> {connection_url}")

engine = create_engine(
    connection_url,
    future=True,
    poolclass=QueuePool,
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class SessionManager:
    """
    This will manage the database sessions.
    """

    inspector: PGInspector = inspect(engine)

    @classmethod
    def get_session(cls) -> Generator[Session, None, None]:
        """
        Get session for the logged in organization.
        """
        try:
            # log.debug("Inside Org session..")

            session = session_local()
            yield session

        except Exception as err:
            log.critical(f"Exception while connecting to database --> {err}")
            raise err

        finally:
            if session is not None:
                session.close()
