import math
from pathlib import Path
import geopandas as gpd
from shapely import Polygon, MultiPolygon

def del_near_point(xy, accuracy) -> list|tuple:
    """
    移除接近的点。

    遍历给定的坐标点列表，根据指定的精度移除过于接近的点，以简化几何形状。

    Args:
    xy (list of tuple): 坐标点列表，每个元素是一个包含x和y坐标的元组。
    accuracy (float): 精度值，用于确定两点之间的最小距离。

    返回:
    list of tuple: 简化后的坐标点列表。
    """
    count = len(xy)
    extXY = [xy[0]]
    for i in range(1, count - 1):
        mid = xy[i]
        back = xy[i + 1]
        back_distance = math.sqrt((mid[0] - back[0]) ** 2 + (mid[1] - back[1]) ** 2)
        if back_distance >= accuracy:
            extXY.append(mid)
    extXY.append(extXY[0])
    return extXY


def nearPoint(data: Path, accuracy: float, save: Path)->list:
    """
    处理地理数据，移除接近的点，并保存结果。

    读取地理数据，对每个几何形状应用del_near_point函数，然后将处理后的数据保存到指定路径。

    args:
    data (Path): 输入数据文件的路径。
    accuracy (float): 精度值，用于del_near_point函数。
    save (Path): 输出数据文件的路径。

    返回:
    list: 保存处理后的数据文件路径。
    """
    gdf = gpd.read_file(data)
    delgdf = gpd.GeoDataFrame(columns=gdf.columns)
    def shan(row):
        if type(row.geometry) == MultiPolygon:
            por = row.geometry.geoms[0]
        else:
            por = row.geometry
        xy = list(zip(por.exterior.xy[0], por.exterior.xy[1]))
        extXY = del_near_point(xy, accuracy)
        inner_coords = []
        if por.interiors:
            for lin in por.interiors:
                interiors_xy = list(zip(lin.xy[0], lin.xy[1]))
                interiorsXY = del_near_point(interiors_xy, accuracy)
                inner_coords.append(interiorsXY)
        if inner_coords:
            delgdf.loc[delgdf.shape[0]] = [*row[:-1], Polygon(extXY, inner_coords)]
        else:
            delgdf.loc[delgdf.shape[0]] = [*row[:-1], Polygon(extXY)]

    gdf.apply(shan, axis=1)
    delgdf = delgdf.set_geometry("geometry")
    delgdf.crs = gdf.crs
    delgdf.to_file(save, encoding="gb18030", crs=gdf.crs)
    stem = save.stem

    return sorted(save.parent.glob(f"{stem}.*"))


if __name__ == "__main__":
    datapath = Path(r"E:\工作文档\测试导出数据\删点测试.shp")
    savepath = Path(r"E:\工作文档\测试导出数据\删除点2.shp")
    nearPoint(datapath, 1, savepath)
