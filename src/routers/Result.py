from pydantic import BaseModel


class Result(BaseModel):
    code: int = 200
    data: dict = {}
    msg: str = ""
