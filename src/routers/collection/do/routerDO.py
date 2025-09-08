from typing import List
from sqlmodel import SQLModel, Relationship
from src.package.database import TYPE


class RouterDO(SQLModel, table=True):
    __tablename__ = "router"
    id: int = TYPE.PRIMARY_KEY
    title: str
    name: str = TYPE.UNIQUE
    path: str | None
    router_type: str | None

    dataItem: List["DataItemDO"] | None = Relationship(
        back_populates="router",
        passive_deletes=True,
        sa_relationship_kwargs={"order_by": "DataItemDO.sort"},
    )  # type: ignore # noqa: F821
