from .service import Service
from package.database.business.DO import BusinessProjectDO


class BusinessProjectService(Service):
    def __init__(self) -> None:
        super().__init__(BusinessProjectDO)


businessProjectService = BusinessProjectService()
