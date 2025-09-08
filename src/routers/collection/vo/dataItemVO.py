from pydantic import BaseModel

class addDataItemArgs(BaseModel):
    title: str
    URL: str | None = None
    path: str | None = None
    color: str = "#79bbff"
    parent_name: str
    router_name: str
    sort: int = None
    is_group: bool

class DataItemArgs(BaseModel):
    id: int = None
    title: str = None
    URL: str = None
    path: str = None
    color: str = None
    parent_name: str = None
    router_name: str = None
    sort: int = None
    is_group: bool = None
    is_public_network:bool = None
