from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from package.utils import re_json

conf = re_json('config.json')

match conf['database']['drivers']:
    case 'sqlite':
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{conf['database']['server']}"
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
    case 'postgresql':
        pass

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
