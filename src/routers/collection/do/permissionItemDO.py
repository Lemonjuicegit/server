from sqlmodel import SQLModel
from src.package.database import TYPE

class PermissionItemDO(SQLModel, table=True):
    __tablename__ = "permission_item"
    
    id:int = TYPE.PRIMARY_KEY
    router_name:int = TYPE.FOREIGN_KEY("router.name")
    permission_name:int = TYPE.FOREIGN_KEY("permission.name")
    deleted:bool = False