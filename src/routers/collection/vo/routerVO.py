from pydantic import BaseModel

class RouterArgs(BaseModel):
    path: str | None = None
    router_name: str | None = None

class RouterUpdate(BaseModel):
    id: int = None
    title: str = None
    path: str = None
    router_type: str = None
