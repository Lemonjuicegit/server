from .service import Service
from package.database.business.DO import BusinessContractDO

class BusinessContractService(Service):
    def __init__(self) -> None:
        super().__init__(BusinessContractDO)


businessContractService = BusinessContractService()
