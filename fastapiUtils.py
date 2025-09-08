import importlib, traceback
import os
from src.routers import store, unzip, log, use, Api, state, zip_list
from src.package.interface.setup import getFunc, setArgs
from pathlib import Path
import importlib

cwd_path = os.getcwd()

def get_router_list():
    router_path = Path(rf"{cwd_path}\src\routers")
    pathlist = router_path.iterdir()
    router_list = []
    for path_ in pathlist:
        if path_.is_dir():
            c_pathlist = path_.iterdir()
            filename = [v.stem for v in c_pathlist if v.is_file()]
            if "app" in filename:
                router_list.append(path_.stem)
    return router_list


def include_router(app, rewrite):
    # 批量挂载路由
    modules = get_router_list()
    modules = [f"src.routers.{v}.app" for v in modules]
    for module in modules:
        imported_module = importlib.import_module(module)
        router_name = module.split(".")[-2]
        if imported_module.router.prefix:
            app.include_router(
                imported_module.router,
                tags=[router_name],
            )
        else:
            app.include_router(
                imported_module.router,
                prefix=f"{rewrite}/{router_name}",
                tags=[router_name],
            )

def split_args(args: str) -> dict:
    args = args.split("&")
    args = list(map(lambda x: x.split("="), args))
    args = dict(args)
    return args

def handle(args, app, query, req):
    """
    处理接口程序
    """
    ip = req.client.host
    func_item = getFunc(args.interArgs["id"])
    imported_module = importlib.import_module(f"{func_item['module']}.setup")
    importlib.reload(imported_module)
    func = getattr(imported_module, func_item["name"])
    file_id = ""
    try:
        if func_item["args"]:
            func_args = setArgs(func_item, args.interArgs, ip, app, store, query, req)
            res = func(*func_args)
        else:
            res = func()
        for v in func_item["return"]:
            match v:
                case "filelist":
                    use.useApi[ip].zipFileName = res
                    name = use.useApi[ip].zipFileName[0].stem
                    zip_list(
                        use.useApi[ip].zipFileName, store.sendPath / ip / f"{name}.zip"
                    )
                    file_id = store.addUseFile(ip, store.sendPath, f"{name}.zip")
                    use.drop_zipFile(ip)
                    use.useApi[ip].zipFileName = []
                    return {"state": state.END, "res": file_id}
                case _:
                    return {"state": state.END, "res": res}
    except Exception as e:
        exc_format = "".join(traceback.format_exception(e))
        log.error(exc_format)
        return {"state": state.ERR, "res": "出现了未处理的问题"}


def reload_module(module_name):
    """递归地重新加载模块"""
    importlib.reload(module_name)  # 重新加载当前模块
    for attr_name in dir(module_name):  # 遍历模块的所有属性
        attr = getattr(module_name, attr_name)
        if isinstance(attr, type(importlib.import_module)):  # 检查是否为模块类型
            sub_module_name = f"{module_name}.{attr_name}"
            reload_module(sub_module_name)  # 递归重新加载子模块


if __name__ == "__main__":
    res = get_router_list()
    print(res)
