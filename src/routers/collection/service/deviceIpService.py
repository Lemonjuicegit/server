from src.routers.collection.service.service import Service
from src.routers.collection.do import DeviceIpDO

class DeviceIpService(Service):
    def __init__(self):
        super().__init__(DeviceIpDO)
        
    def getIpList(self):
        res = super().select({"grant":1})
        ip_list = [i.ip for i in res]
        return ip_list

deviceIpService = DeviceIpService()