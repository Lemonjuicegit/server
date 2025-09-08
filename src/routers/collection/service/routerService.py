from src.routers.collection.service.service import Service
from src.routers.collection.do import RouterDO
from src.routers.utils import handleTree

class RouterService(Service):
    def __init__(self):
        super().__init__(RouterDO)

    def getDataItemTree(self, path,is_public_network=0):
        res = super().select({"path": path})
        if is_public_network:
            data_item = [dict(x) for x in res[0].dataItem if x.is_public_network==1]
        else:
            data_item =[dict(x) for x in res[0].dataItem]

        result = handleTree(data_item, id="name", parentId="parent_name")

        return {**dict(res[0]), "dataItem": result}

    def getDataTree(self):
        router = super().select({"router_type": "collection"})
        result = {}
        for row in router:
            data_item = [dict(x) for x in row.dataItem]
            tree = handleTree(data_item, id="name", parentId="parent_name")
            result[row.name] = {**dict(row), "dataItem": tree}
        return result


routerService = RouterService()
