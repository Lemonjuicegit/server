from sqlmodel import SQLModel
from package.database import TYPE
from datetime import date


class BusinessUserColumnDO(SQLModel, table=True):
    __tablename__ = "business_user_column"
    id: int = TYPE.PRIMARY_KEY
    core_column_id: int
    user_id: int
    search: int
    hidden: int
    deleted: int
    creator: int
    updater: str
    create_time: date
    update_time: date
    view: str
