from uuid import uuid4

from fastapi import  APIRouter,Request
from pydantic import BaseModel
from .exf import lq_exf,hc_exf
from .. import state,store,use,zip_list
router = APIRouter()

class Args(BaseModel):
    gdb: str=''
    state:int=0
    
@router.post("/lqexf")
async def lqexf(args: Args,req: Request=None):
    ip = req.client.host
    gdb = store.useFile[store.useFile.filename == args.gdb].path.values[0]
    if args.state == 0:
        use.useApi[ip].lqexf_generate = lq_exf(gdb,store.sendPath / ip)
    try:
        exf_state,res = next(use.useApi[ip].lqexf_generate)
    except StopIteration:
        zip_list(use.useApi[ip].zipFileName,store.sendPath / ip/'林权exf.zip')
        file_id = store.addUseFile(ip, store.sendPath, "林权exf.zip")
        use.drop_zipFile(ip)
        use.useApi[ip].zipFileName = []
        return {"state":state.END,"res":'林权exf生成成功!','fileID':file_id}
    if exf_state == state.ERR:
        use.useApi[ip].lqexf_generate = None
        return {"state":exf_state,"res":res}
    if exf_state == state.RES:
        use.useApi[ip].zipFileName.append(store.sendPath / ip / res)
        return {"state":exf_state,"res":res}
@router.post("/hcexf")
async def hcexf(args: Args,req: Request=None):
    ip = req.client.host
    gdb = store.query(f"filename == '{args.gdb}'",'path')
    if args.state == 0:
        use.useApi[ip].hcexf_generate = hc_exf(gdb,store.sendPath / ip)
    try:
        exf_state,res = next(use.useApi[ip].hcexf_generate)
    except StopIteration:
        zip_list(use.useApi[ip].zipFileName,store.sendPath / ip/ f"{gdb.stem}.zip")
        file_id = store.addUseFile(ip, store.sendPath,f"{gdb.stem}.zip")
        use.drop_zipFile(ip)
        use.useApi[ip].zipFileName = []
        return {"state":state.END,"res":file_id}
    if exf_state == state.ERR:
        use.useApi[ip].hcexf_generate = None
        return {"state":exf_state,"res":res}
    if exf_state == state.RES:
        use.useApi[ip].zipFileName.append(store.sendPath / ip / res)
        return {"state":exf_state,"res":res}

    