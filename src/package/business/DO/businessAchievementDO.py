from sqlmodel import SQLModel, Relationship

from package.database import TYPE


class BusinessAchievementDO(SQLModel, table=True):
    __tablename__ = "business_achievement"
    id: int = TYPE.PRIMARY_KEY
