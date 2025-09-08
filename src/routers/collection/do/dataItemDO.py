from sqlmodel import SQLModel, Relationship
from .routerDO import RouterDO
from src.package.database import TYPE


class DataItemDO(SQLModel, table=True):
    __tablename__ = "data_item"

    id: int = TYPE.PRIMARY_KEY
    title: str
    name: str = TYPE.UNIQUE
    URL: str | None
    path: str | None
    color: str = "#79bbff"
    parent_name: str
    router_name: str = TYPE.FOREIGN_KEY("router.name")
    sort: int
    is_group: bool = False
    is_public_network:bool = False

    router: RouterDO | None = Relationship(back_populates="dataItem")
