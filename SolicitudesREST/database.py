from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL="mysql+pymysql://user_titulatec:TitulaTEC.123@localhost/TitulaTEC"

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        return db
    finally:
        db.close()