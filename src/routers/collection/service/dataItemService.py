from src.routers.collection.service.service import Service
from src.routers.collection.do import DataItemDO
class DataItemService(Service):
    def __init__(self):
        super().__init__(DataItemDO)

dataItemService = DataItemService()
