from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from .const import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base: DeclarativeMeta = declarative_base()

metadata: MetaData = MetaData()

engine = create_engine(DATABASE_URL)
