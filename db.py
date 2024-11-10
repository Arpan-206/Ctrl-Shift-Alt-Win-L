from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine


# Postgres
SQLiteDatabaseURL = "sqlite:///./database.db"
engine = create_engine(SQLiteDatabaseURL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
