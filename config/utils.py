from sqlalchemy.orm import Session, sessionmaker

from .database import engine

session_maker = sessionmaker(bind=engine)


def get_session() -> Session:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
