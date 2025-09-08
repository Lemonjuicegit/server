import socket
import requests
import pandas as pd
import json, os
from pathlib import Path
def getServerIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要连接到真正的服务器，只需要尝试解析主机名即可触发IP配置的查询
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def groupby(df: pd.DataFrame, by: list[str], agg: str):
    """agg:[
        'any','all','count','cov','first','idxmax',
        'idxmin','last','max','mean','median','min',
        'nunique','prod','quantile','sem','size',
        'skew','std','sum','var'
    ]
    """
    Aggfield = agg.upper()
    df2 = df.copy()
    df2[Aggfield] = ""
    by_df = pd.DataFrame(df2.groupby(by=by)[Aggfield].agg(agg))
    res_df = pd.merge(df, by_df, on=by[0], how="left")
    return res_df

def re_json(jsonpath):
    """将字典转换为json字符串，并格式化"""
    with open(jsonpath, "r", encoding="utf-8") as f:
        res = json.loads(f.read())
    return res

def send_get(url,**kwargs):
    argv = '?'
    for k, v in kwargs.items():
        argv += f'{k}={v}&'
    return requests.get(url+argv[:-1]).json()