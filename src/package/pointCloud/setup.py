import numpy as np
import geopandas as gpd
import laspy
from shapely.geometry import Point
from pathlib import Path
import dask.array as da


# 点云提取点

def getPointCloudXYZ(las_file: str | Path):
    xyz = np.array([])
    las = laspy.read(las_file)
    for i in range(len(las.x)):
        xyz = np.append(xyz, [las.x[i], las.y[i], las.z[i]])


def las_apply(las_file: str | Path, callback):
    las = laspy.read(las_file)
    for i in range(len(las.x)):
        return callback([las.x[i], las.y[i], las.z[i]])


def las_density(xyz, gdf):
    point = Point(xyz[0] + 36000000, xyz[1])
    polygon = gdf.loc[0].geometry
    if polygon.contains(point):
        return True
    return False


def dask_apply(data, callback):
    dask_array = da.from_array(data)
    lambda_square = lambda x: callback(x)
    result_dask_array = dask_array.map_blocks(lambda_square)
    result_array = result_dask_array.compute()
    return result_array


if __name__ == "__main__":
    is_poi = []
    las_dir = r"E:\工作文档\万州区\水资源\点云"
    files = Path(las_dir).glob("*.las")
    shp = r"E:\工作文档\万州区\鱼背山水库管理线及保护线shp\鱼背山水库.shp"
    gdf = gpd.read_file(shp)

    # las = laspy.read(list(files)[2])
    # np_xy = np.column_stack((np.array(las.x) + 36000000, np.array(las.y)))
    def callback_(data):
        res_ = ""
        for zb in range(len(data)):
            res_ += f"{round(zb[0]+36000000,2)},{round(zb[1],2)},{round(zb[2],2)}\n"
        return res_

    def eq_poi(files_):
        las = laspy.read(files_)
        res_ = ""
        for i in range(len(las.x)):
            res_ += f"{round(las.x[i]+36000000,2)},{round(las.y[i],2)},{round(las.z[i],2)}\n"
        return res_

    # result_array = dask_apply(np.array([str(v) for v in files]), eq_poi)
    with open(r"E:\工作文档\万州区\水资源\点云\点云2.xyz", "a") as f:
        for i in files:
            f.write(eq_poi(i))
            print(i)
