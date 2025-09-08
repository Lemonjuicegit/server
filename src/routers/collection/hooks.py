import importlib
from pathlib import Path
from fastapiUtils import cwd_path

def get_controller():
    controller_path = Path(rf"{cwd_path}\src\routers\collection\controller")
    pathlist = controller_path.iterdir()
    return [x.stem for x in pathlist if x.stem not in ["__init__", "__pycache__"]]

def include_router(router):
    modules = get_controller()
    modules = [f"src.routers.collection.controller.{v}" for v in modules]
    for module in modules:
        imported_module = importlib.import_module(module)
        tag = module.split(".")[-1]
        router.include_router(
            imported_module.router,
            prefix=f"/{tag}",
            tags=[tag],
        )
