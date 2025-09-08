from .service import Service
from package.database.business.DO import BusinessCoreColumnDO


class BusinessCoreColumnService(Service):
    def __init__(self) -> None:
        super().__init__(BusinessCoreColumnDO)


businessCoreColumnService = BusinessCoreColumnService()
