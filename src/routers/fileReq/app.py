from fastapi import BackgroundTasks, APIRouter, File, Request, UploadFile
from starlette.responses import FileResponse
from src.routers import store, state, log, unzip
from src.routers import Result

router = APIRouter(prefix="/file-req")


@router.post(f"/upload")
async def create_file(file: UploadFile = File(), req: Request = None):
    ip = req.client.host
    log.info("upload:%s-%s", ip, file.filename)
    file_content = await file.read()
    filename = file.filename
    extractpath = store.uploadPath / ip / filename
    file_id = store.addUseFile(ip, store.uploadPath, filename)
    with open(extractpath, "wb") as buffer:
        buffer.write(file_content)
    return Result(data={"fileID": file_id})


@router.post(f"/upload_zip")
async def create_upload_file(
    file: UploadFile = File(), filetype: str = "", req: Request = None
):
    ip = req.client.host
    log.info("upload:%s-%s", ip, file.filename)
    file_content = await file.read()
    filename = file.filename
    extractpath = store.uploadPath / ip / filename
    center_id = store.addUseFile(ip, store.uploadPath, filename)
    res = {"center_file_id": center_id, "engender": []}
    with open(extractpath, "wb") as buffer:
        buffer.write(file_content)
    if filetype == "gdb":
        unzip(extractpath, store.uploadPath / ip)
        engender = store.addUseFile(
            ip, store.uploadPath, f"{filename.split('.')[0]}.gdb"
        )
        res["engender"] = engender
        return res
    if filetype == "zip":
        namelist = unzip(extractpath, store.uploadPath / ip / file.filename)
        for f in namelist:
            res["engender"].append(store.addUseFile(ip, store.uploadPath, f))
    elif filetype == "shp":
        filelist = unzip(extractpath, store.uploadPath / ip)
        for f in filelist:
            if f.endswith(".shp"):
                res["shp"] = store.addUseFile(ip, store.uploadPath, f)
                res["engender"].append(res["shp"])
                continue
            res["engender"].append(store.addUseFile(ip, store.uploadPath, f))
    return res


@router.post(f"/download")
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


@router.delete(f"/delete")
def delete_file(fileid, task: BackgroundTasks):
    task.add_task(store.drop_query, f"ID == '{fileid}'")
    return Result()
