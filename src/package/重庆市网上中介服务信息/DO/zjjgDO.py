from sqlmodel import SQLModel
from src.package.database import TYPE
from typing import Optional
from datetime import date
import uuid

class ZjjgDO(SQLModel, table=True):
    __tablename__ = "zjjg"
    id: uuid.UUID = TYPE.PRIMARY_KEY
    zjjgmc:Optional[str] = None
    jglx:Optional[str] = None
    fwlx:Optional[str] = None
    zcd:Optional[str] = None
    link:Optional[str] = None
    rksj:Optional[date] = None
    bgdz:Optional[str] = None
    lzr:Optional[str] = None
    lxyx:Optional[str] = None


