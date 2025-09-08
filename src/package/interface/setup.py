import json
from typing import Any, List
from typing import Any, List
from pathlib import Path
from typing import List

cwdpath = Path(__file__).parent / "interface.json"

interface_json = json.loads(cwdpath.read_text(encoding="utf-8"))


def getInterface():
    interface_data = json.loads(cwdpath.read_text(encoding="utf-8"))
    return interface_data["interface"]


def Select_id():
    def recursion(children, depth="", result=None):
        if result is None:
            result = {}
        for index, item in enumerate(children):
            if item["child"]:
                result[item["id"]] = f"{depth}-{index}" if depth else str(index)
            else:
                result[item["id"]] = f"{depth}-{index}" if depth else str(index)
                recursion(item["children"], index, result)
        return result

    res = recursion(getInterface())
    interface_json["select_id"] = res
    with cwdpath.open("w", encoding="utf-8") as f:
        f.write(json.dumps(interface_json))


def getFunc(select_id: List[int]):
    res = None
    for index in select_id:
        if res is None:
            res = getInterface()[int(index)]
        else:
            res = res["children"][int(index)]
    return res


def upInterface(inter_json):
    with open(cwdpath, "w", encoding="utf-8") as f:
        f.write(json.dumps({"interface": inter_json}))


def setArgs(func_item, interArgs, ip, app, store, query, req) -> List[Any]:
    args_dict = {
        "ip": ip,
        "app": app,
        "store": store,
        "query": query,
        "req": req,
    }
    func_args = []
    n = 0  # 记录已取得第几个服务端参数
    for k, v in enumerate(func_item["args"]):
        match v:
            case x if x in args_dict.keys():
                func_args.append(args_dict[x])
            case "int":
                func_args.append(int(interArgs["args"][n]))
                n += 1
            case "float":
                func_args.append(float(interArgs["args"][n]))
                n += 1
            case "upload":
                func_args.append(
                    store.uploadPath / ip / store.file_id(interArgs["args"][n], "path")
                )
                n += 1
            case "send":
                func_args.append(store.sendPath / ip / interArgs["args"][n])
                n += 1
            case _:
                func_args.append(interArgs["args"][k])
                n += 1
    return func_args


if __name__ == "__main__":
    # Select_id()
    getFunc("3")
