from sqlmodel import SQLModel
from package.database import TYPE
from datetime import date


class BusinessCoreColumnDO(SQLModel, table=True):
    __tablename__ = "business_core_column"
    id: int = TYPE.PRIMARY_KEY
    module: str
    column_name: str
    column_cn: str
    searchable: int
    column_type: str
    search_type: str
    condition: str
    dic_id: int
    deleted: int
    creator: str
    updater: str
    create_time: date
    update_time: date
    sort: int
    original: int
    parent_name: str
    formatter: str
    viewable: int
    min_width: int
    param_type: str
    date_formatter: str
    number_formatter: str
