from .service import Service
from package.database.business.DO import BusinessCustomerDO


class BusinessCustomerService(Service):
    def __init__(self) -> None:
        super().__init__(BusinessCustomerDO)


businessCustomerService = BusinessCustomerService()
