from .service import Service
from package.database.business.DO import BusinessUserColumnDO


class BusinessUserColumnService(Service):
    def __init__(self) -> None:
        super().__init__(BusinessUserColumnDO)


businessUserColumnService = BusinessUserColumnService()
