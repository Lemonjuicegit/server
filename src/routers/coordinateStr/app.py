import json
from uuid import uuid4
from fastapi import  APIRouter,Request
from pydantic import BaseModel
from .. import store,state,zip_list
from . import gardens
from pathlib import Path

router = APIRouter()

class Args(BaseModel):
    shp: str=''
    templaet:int=0
    
current = Path(store.cwdpath)/ 'src' / 'routers' / 'coordinateStr'
templaet_list = json.loads((Path(current) / 'template.json').read_text(encoding="utf-8"))
@router.post("/coordinate-str-txt")
async def coordinate_str(args:Args,req: Request):
    ip = req.client.host
    jd = store.sendPath / ip / '节点.shp'
    file_id = str(uuid4())
    shp_path = store.useFile[store.useFile.filename == f'{args.shp}.zip']
    if not shp_path.shape[0]:
        return {'state':state.ERR,'res':'未找到该文件'}
    gar = gardens(jd,shp_path.path.values[0],templaet_list[args.templaet])
    shpfiles =list((store.sendPath / ip).glob('节点.*'))
    gar.get_coordinate_string(store.sendPath / ip / f'{args.shp}.txt')
    shpfiles.append(store.sendPath / ip / f'{args.shp}.txt') 
    zip_list(shpfiles,store.sendPath / ip / f"{args.shp}.zip")
    store.addUseFile(ip,store.sendPath,f'{args.shp}.zip',file_id)
    for shpfile in shpfiles:
        shpfile.unlink()
    return {'state':state.END,'res':'txt坐标串完成','fileID':file_id}


