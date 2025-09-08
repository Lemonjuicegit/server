from sqlmodel import Field, Session, SQLModel, create_engine, select

class Result(SQLModel):
    code:int = 200
    data: list | dict = []
    msg: str = ''