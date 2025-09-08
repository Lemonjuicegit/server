from fastapi import APIRouter,Request
from uuid import uuid4
from src.routers.collection.vo import RouterArgs, RouterUpdate
from src.routers.collection.service import routerService
from src.routers.collection.result import Result

router = APIRouter()

@router.post("/router")
def routerControllerOne(args: RouterArgs):
    res = routerService.select({"path": args.path})
    return res[0]

@router.get("/item_tree")
def getDataItemTree(args: str,req: Request):
    network_name = req.headers.get('Network-Name')
    public_network_ip = ['183.71.245.98','localhost']
    if network_name in public_network_ip:
        res = routerService.getDataItemTree(args,is_public_network=1)
    else:
        res = routerService.getDataItemTree(args)
    return Result(data=res)


@router.get("/tree")
async def getTree():
    res = routerService.getDataTree()
    return Result(data=res)


@router.post("/add")
def addRtouter(data: RouterUpdate):
    name = uuid4().hex
    routerService.insert([{**dict(data), "name": name}])
    res = routerService.select({"name": name})
    return Result(data=res)


@router.post("/update")
def upRouter(data: RouterUpdate):
    routerService.update([data.model_dump(exclude_unset=True)])
    return Result()


@router.delete("/delete")
def deleteDataItem(del_id: list[int]):
    routerService.delete(del_id)
    return Result()


@router.get("/eq_path")
def getPathList(path: str):
    res = routerService.select_all()
    path_list = [v.path for v in res]
    if path in path_list:
        return Result()
    else:
        return Result(code=404, msg="请求的网址不存在")


@router.get("/list")
def getList():
    res = routerService.select({"router_type": "collection"})
    return Result(data=res)
