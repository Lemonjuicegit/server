from pathlib import Path
import traceback
import sys
from fastapi import FastAPI, Query, Request, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from src.routers import store, unzip, log, use, Api, state
from fastapiUtils import include_router, handle, cwd_path
from src.routers.collection.common.token import create_access_token
from src.routers.collection.result import Result
from src.routers.collection.service import deviceIpService, routerService

# 入口程序

ip_list = deviceIpService.getIpList()
manage_dir_absolute = f"{cwd_path}\\manage"
assets_manage_absolute = fr"{cwd_path}\manage\assets"
assets_manage_absolute_test = fr"{cwd_path}\manage_test\assets"
if sys.argv[1] in ['1','3']:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/assets", StaticFiles(directory=assets_manage_absolute), name="assets")
    rewrite = ""
elif sys.argv[1] == '2':
    app = FastAPI()
    app.mount("/assets", StaticFiles(directory=assets_manage_absolute_test), name="assets")
    rewrite = ""
else:
    app = FastAPI()
    rewrite = ""

@app.middleware("http")
async def check_static_access(request: Request, call_next):
    ip = request.client.host
    Path(store.uploadPath / ip).mkdir(exist_ok=True, parents=True)
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
include_router(app, rewrite)

class Args(BaseModel):
    xm_name: str = ""
    menuitemURL: dict = {}
    menuitem: dict = {}
    data: list = []
    menuitemName: str = ""
    title: str = ""
    id: int = 0
    routerName: str = ""
    reviseRouterName: str = ""
    usdel: int = 0
    interArgs: dict = {}

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    exc_format = "".join(traceback.format_exception(exc))
    log.error(exc_format)
    return {"state": state.ERR, "res": f"服务出错了!,请联系管理员!{exc}"}

@app.post(f"{rewrite}/add_use")
async def add_use(req: Request):
    ip = req.client.host
    use.useApi[ip] = Api(ip)
    (store.sendPath / ip).mkdir(exist_ok=True, parents=True)
    log.info("%s连接", ip)
    return 1

@app.get(f"{rewrite}/ip_access_authorization")
async def ip_access_authorization(args_ip:str):
    ip_access = ['localhost', '192.168.2.139','192.168.2.50','183.71.245.98']
    if  args_ip not in ip_access:
        return {"state": state.ERR, "res": "禁止访问非授权地址。"}
    else:
        return {"state": state.RES, "res": "成功"}

@app.get(f"{rewrite}/disconnect")
async def use_disconnect(req: Request = None):
    ip = req.client.host
    store.drop_query(f"ip == '{ip}'")
    log.info("%s断开", ip)

@app.post(f"{rewrite}/upload")
async def create_upload_file(
    file: UploadFile = File(), filetype: str = "", req: Request = None
):
    ip = req.client.host
    log.info("upload:%s-%s", ip, file.filename)
    file_content = await file.read()
    filename = file.filename
    suffix = filename.split(".")[-1]
    upload_dir = store.uploadPath / ip
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_id = store.addUseFile(ip, store.uploadPath, filename)
    file_id_name = f"{file_id}.{suffix}"
    upload_path = upload_dir / file_id_name
    res = {"center_file_id": file_id, "engender": []}

    with open(upload_path, "wb") as buffer:
        buffer.write(file_content)
    if filetype == "gdb":
        unzip(upload_path, upload_dir)
        engender_id = store.addUseFile(
            ip, store.uploadPath, file_id_name
        )
        res["engender"] = engender_id
        return res
    if filetype == "zip":
        namelist = unzip(upload_path, upload_dir)
        for f in namelist:
            res["engender"].append(store.addUseFile(ip, store.uploadPath, f))
    elif filetype == "shp":
        filelist = unzip(upload_path, upload_dir)
        for f in filelist:
            if f.endswith(".shp"):
                res["shp"] = store.addUseFile(ip, store.uploadPath, f)
                res["engender"].append(res["shp"])
                continue
            res["engender"].append(store.addUseFile(ip, store.uploadPath, f))
    return res

@app.post(f"{rewrite}/download")
async def create_download_file(fileid, isdel, req: Request, task: BackgroundTasks):
    ip = req.client.host
    log.info("create_download_file:%s", ip)
    # 查找要下载的文件
    path = store.file_id(fileid, "path")
    if int(isdel):
        task.add_task(store.drop_query, f"ID == '{fileid}'")
    if path:
        return FileResponse(path, filename=path.name)
    return state.ERR


async def cell(args: Args, query=Query(None), req: Request = None):
    res = handle(args, app, query, req)
    return res

@app.get("/get_user")
async def get_user(req: Request):
    ip = req.client.host
    token = create_access_token({"ip": ip})
    device = deviceIpService.select({"ip": ip})
    if not device:
        deviceIpService.insert([{"ip": ip,"title":"未知设备","name":token,"grant":1}])
        device = deviceIpService.select({"ip": ip})
    return Result(data={"accessToken": token, "device": device[0]})

if sys.argv[1] in ['1','3']:
    @app.get("/{xm_name}")
    async def getHtml(xm_name):
        res = routerService.select_all()
        path_list = [v.path for v in res]
        path_list = [*path_list,'onlineMediatorsView']
        if xm_name == "home":
            return FileResponse(f"{cwd_path}/home/index.html")
        elif xm_name in path_list:
            return FileResponse(rf"{cwd_path}/manage/index.html")
elif sys.argv[1] == '2':
    @app.get("/{xm_name}")
    async def getHtml(xm_name):
        res = routerService.select_all()
        path_list = [v.path for v in res]
        if xm_name == "home":
            return FileResponse(f"{cwd_path}/ststic/index.html")
        elif xm_name in path_list:
            return FileResponse(rf"{cwd_path}/manage_test/index.html")
        
@app.get("/stream/progress")
async def stream_progress():
    async def generate():
        for i in range(100):
            yield f"data: Progress: {i + 1}%\n\n"
        yield "data: Task completed!\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    if sys.argv[1] in ['1','2']:
        uvicorn.run(app, host="192.168.2.50", port=45454)
    else:
        uvicorn.run(app, host="192.168.2.71", port=45454)

