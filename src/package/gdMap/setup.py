from typing import List
import math
import requests, json
import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import Polygon, MultiPolygon, LineString, Point

gd_key = ["c09c99c9d77160b95d1931026eb0d14f", "39ac36d228ade6d9b068ee131785d036"]


def getURL(shppath, types):
    if isinstance(shppath, MultiPolygon):
        por = shppath.geoms[0]
    else:
        por = shppath
    xy = list(zip(por.exterior.xy[0], por.exterior.xy[1]))
    xy = [f"{round(v[0],6)},{round(v[1],6)}" for v in xy]
    coordinateStr = "|".join(xy)
    types_str = "|".join(types)
    url = f"https://restapi.amap.com/v3/place/polygon?polygon={coordinateStr}&key=c09c99c9d77160b95d1931026eb0d14f&types={types_str}"
    return url

def getPoi(url):
    res = requests.get(url, timeout=20)
    res = json.loads(res.content)
    return res


def getPlaceData(url):
    """
    发送请求到指定URL，获取地点数据并解析为GeoDataFrame。

    参数:
    - url: 请求的URL

    返回:
    - 解析后的GeoDataFrame对象
    """
    res = requests.get(url, timeout=20)
    res = json.loads(res.content)
    gdf = point_poi(res)
    return gdf


def point_poi(poi):
    """
    将JSON格式的地点信息解析为GeoDataFrame。

    参数:
    - poi: 包含地点信息的JSON对象

    返回:
    - GeoDataFrame对象，包含解析后的地点数据
    """
    fields = [
        "address",
        "pname",
        "biz_type",
        "cityname",
        "type",
        "photos",
        "typecode",
        "shopinfo",
        "adname",
        "timestamp",
        "name",
        "location",
        "tel",
        "id",
        "geometry",
    ]
    gdf = gpd.GeoDataFrame(columns=fields, crs="EPSG:4490")
    temp = {}
    for v in poi["pois"]:
        temp = v
        temp["photos"] = [p["url"] for p in v["photos"]]
        point = Point(*v["location"].split(","))
        gdf.loc[len(gdf)] = [*[str(temp[key]) for key in fields[:-1]], point]
    return gdf


def poi_concat(poi_file_path: List[Path | dict], save):
    """
    合并多个文件或字典中的地点数据，并保存为GeoDataFrame。

    参数:
    - poi_file_path: 包含地点数据的文件路径列表或字典列表
    - save: 保存结果的文件路径

    返回:
    - 合并后的GeoDataFrame对象
    """
    merge_poi = {}
    for poi_data in poi_file_path:
        if isinstance(poi_data, Path):
            poi = json.loads(poi_data.read_text(encoding="utf-8"))
        else:
            poi = poi_data

        if poi["pois"]:
            if merge_poi:
                merge_poi["pois"] = [*merge_poi["pois"], *poi["pois"]]
            else:
                merge_poi = poi_data
    res_gdf: gpd.GeoDataFrame = point_poi(merge_poi)
    res_gdf.to_file(save, encoding="gb18030")


def getPlaceData_cll(shppath, types, save):
    """
    根据多边形路径和类型获取地点数据，并保存结果。

    参数:
    - shppath: 多边形路径的文件路径
    - types: 地点类型列表
    - save: 保存结果的文件路径

    返回:
    - 保存结果的文件路径列表
    """
    gdf = gpd.read_file(shppath)
    res_gdf = None
    for _, row in gdf.iterrows():
        url = getURL(row.geometry, types)
        temp = getPlaceData(url)
        if temp.shape[0] == 0:
            continue
        if res_gdf:
            res_gdf = gpd.concat([res_gdf, temp])
        else:
            res_gdf = temp
    name = save.stem
    res_gdf.to_file(save, encoding="gb18030")
    return list(save.parent.glob(f"{name}.*"))


def geocoding(dz_data, save, save_excel, key):
    """
    地理编码：将地址数据转换为地理坐标，并保存结果。

    参数:
    - dz_data: 地址数据的Excel文件路径
    - save: 保存结果的文件路径
    - save_excel: 保存结果的Excel文件路径
    - key: 高德地图API密钥的索引
    """
    df = pd.read_excel(dz_data)
    fields = ["MC", "DZ", "geometry"]
    gdf = gpd.GeoDataFrame(columns=fields, crs="EPSG:4490")
    data_df = pd.DataFrame(columns=["MC", "DZ", "X", "Y"])
    for _, row in df.iterrows():
        dz_list = row["DZ"].split("、")
        for dz in dz_list:
            url = f"https://restapi.amap.com/v3/geocode/geo?address={dz}&city=重庆&key={gd_key[key]}"
            res = json.loads(requests.get(url, timeout=20).content)
            if res["geocodes"]:
                for v in res["geocodes"]:
                    x = float(v["location"].split(",")[0])
                    y = float(v["location"].split(",")[1])
                    gdf.loc[len(gdf)] = [row["MC"], row["DZ"], Point(x, y)]
                    data_df.loc[len(data_df)] = [row["MC"], row["DZ"], x, y]
    gdf.to_file(save, encoding="gb18030")
    data_df.to_excel(save_excel)


def getPlaceURL(keywords, types, city, page, key):
    url = f"https://restapi.amap.com/v3/place/text?keywords={keywords}&types={types}&city={city}&offset=25&page={page}&key={key}&extensions=all"
    return url


def getPoiJson(save, urlCallback):
    """
    获取地点数据并保存为JSON文件。

    参数:
    - save: 保存结果的文件路径
    - urlCallback: 生成URL的回调函数
    """
    url = urlCallback(1)
    res = requests.get(url, timeout=20)
    merge_poi = json.loads(res.content)
    if merge_poi["pois"]:
        for v in range(1, math.ceil(int(merge_poi["count"]) / 25)):
            url = urlCallback(1 + v)
            res = requests.get(url, timeout=20)
            res = json.loads(res.content)
            merge_poi["pois"] = [*merge_poi["pois"], *res["pois"]]
        with open(save, "w", encoding="utf-8") as f:
            f.write(json.dumps(merge_poi, ensure_ascii=False))


if __name__ == "__main__":
    getPoiJson(
        r"E:\工作文档\测试导出数据\poi\农家乐poi.json",
        lambda i: getPlaceURL(
            "农家乐", "", "云阳县", i, "39ac36d228ade6d9b068ee131785d036"
        ),
    )

    # poilist = []
    # for i in range(1,5):
    #     jsonpath = Path(f"E:\\工作文档\\测试导出数据\\poi\\新建文件夹 (2)\\{i}.json")
    #     res2 = json.loads(jsonpath.read_text(encoding="utf-8"))
    #     print(len(res2["pois"]))
    #     poilist.append(res2)
    # poi_concat(poilist, r"E:\工作文档\测试导出数据\poi\农庄.shp")
