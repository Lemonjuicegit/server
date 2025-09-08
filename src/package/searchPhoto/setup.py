from sqlite3 import connect
import uuid,os
import pandas as pd
from pathlib import Path
from . import store

cnn = connect('db.sqlite3')
cursor = cnn.cursor()


def search_picture(zj:list[str]):
    picture_data = {"title":"耕地非粮化举证","permissions":0,"data":[]}
    for v in zj:
        res = list(cursor.execute(f"SELECT ZJMC FROM SPB_XZQDM WHERE XZQDM = '{v}'"))
        if not res:
            return picture_data
        ZJMC = res[0][0]
        picture_data["data"].append({"title":ZJMC,"name":str(uuid.uuid4()),"child": False,"children":[]})
        res = cursor.execute(f"SELECT * FROM GD_FLH_picture WHERE XZQDM = '{v}'")
        temp = {}
        for row in res:
            if row[2] not in temp.keys():
                temp[row[2]] = [{
                    "title": row[4],
                    "name": row[0],
                    "URL": f"http://{store.serverip}/{row[2]}/{row[4]}",
                }]
            else:
                temp[row[2]].append({
                    "title": row[4],
                    "name": row[0],
                    "URL": f"http://{store.serverip}/{row[2]}/{row[4]}",
                })
        picture_data["data"][len(picture_data["data"])-1]["children"] = [
            {
                "title":key,
                "tbbh":key,
                "name":str(uuid.uuid4()),
                "child": True,
                "URLS":value,
                "path": "/FlhSearch",
            } for key,value in temp.items()]
    
    return picture_data