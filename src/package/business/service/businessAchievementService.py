from .service import Service
from package.database.business.DO import BusinessAchievementDO


class BusinessAchievementService(Service):
    def __init__(self) -> None:
        super().__init__(BusinessAchievementDO)


businessAchievementService = BusinessAchievementService()
