from fastapi import APIRouter, Request
from uuid import uuid4
from src.routers.collection.vo import addDataItemArgs, DataItemArgs
from src.routers.collection.result import Result
from src.routers.collection.service import dataItemService

router = APIRouter()

@router.get("/list")
def getDataItemList():
    res = dataItemService.select_all()
    return Result(data=res)

@router.post("/select")
def getDataItem(args: DataItemArgs):
    return dataItemService.select(args.model_dump(exclude_unset=True))

@router.post("/add")
def addDataItem(args: addDataItemArgs):
    name = uuid4().hex
    dataItemService.insert([{**dict(args), "name": name}])
    res = dataItemService.select({"name": name})
    return Result(data=res)

@router.post("/update")
def updateItem(args: list[DataItemArgs]):
    dataItemService.update([v.model_dump(exclude_unset=True) for v in args])
    return Result()

@router.delete("/delete")
def deleteItem(del_id: list[int]):
    dataItemService.delete(del_id)
    return Result()