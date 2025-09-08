from fastapi import  APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.package.重庆市网上中介服务信息.database import cggg_service,jggg_service,zjjg_service
from src.package.重庆市网上中介服务信息.setup import insert_cggg,insert_jggg
from src.routers.onlineMediators.convert import convert_list
router = APIRouter()

class Args(BaseModel):
    service_type_name:str = ''
    select_time:Optional[list[datetime]] = None

@router.post("/cggg")
def get_cggg(args:Args):
    # args_dict = args.model_dump(exclude_unset=True)
    if not args.select_time:
        res = cggg_service.limit()
    else:
        # 对用户输入进行转义以防止SQL注入
        escaped_service_type = args.service_type_name.replace('%', '\\%').replace('_', '\\_')
        where = lambda x: (
            x.where(cggg_service.DO.service_type_name.like(f"%{escaped_service_type}%"))
            .where(cggg_service.DO.time_announcement >= args.select_time[0])
            .where(cggg_service.DO.time_announcement <= args.select_time[1])
        )
        res = cggg_service.select(where)
    return convert_list(res)


@router.post("/jggg")
def get_jggg(args:Args):
    if not args.select_time:
        res = jggg_service.limit()
    else:
        # 对用户输入进行转义以防止SQL注入
        escaped_service_type = args.service_type_name.replace('%', '\\%').replace('_', '\\_')
        where = lambda x: (
            x.where(jggg_service.DO.service_type_name.like(f"%{escaped_service_type}%"))
            .where(jggg_service.DO.select_time >= args.select_time[0])
            .where(jggg_service.DO.select_time <= args.select_time[1])
        )
        res = jggg_service.select(where)
    return convert_list(res)

@router.post("/zjgg")
def get_zjjg(args:Args):
    if not args.service_type_name:
        res = zjjg_service.limit()
    else:
        # 对用户输入进行转义以防止SQL注入
        escaped_service_type = args.service_type_name.replace('%', '\\%').replace('_', '\\_')
        where = lambda x: x.where(zjjg_service.DO.fwlx.like(f"%{escaped_service_type}%"))
        res = zjjg_service.select(where)
    return convert_list(res)

@router.get("/update")
def update():
    try:
        insert_cggg()
        insert_jggg()
    except Exception as e:
        return False
    return True