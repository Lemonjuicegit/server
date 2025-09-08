import geopandas as gpd
import numpy as np
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

def areaEqually(
    XZQArea: str,
    Area_shp: str,
    XZQ_key: str,
    Area_key: str,
    XZQ_area_field: str,
    Area_shp_field: str,
    precision:str
) -> gpd.GeoDataFrame:
    """
    根据行政区划面积和兴趣区域面积进行面积分配。

    Args:
    - XZQArea: 行政区划面积数据路径
    - Area_shp: 兴趣区域面积数据路径
    - XZQ_key: 行政区划数据的关键字段
    - Area_key: 兴趣区域数据的关键字段
    - XZQ_area_field: 行政区划数据中的面积字段
    - Area_shp_field: 兴趣区域数据中的面积字段
    - precision: 面积计算的精度

    返回:
    - gpd.GeoDataFrame: 经过面积分配处理的GeoDataFrame
    """
    XZQArea_path = Path(XZQArea)
    Area_shp_path = Path(Area_shp)
    def compute(x):
        return Decimal(x).quantize(Decimal(precision), ROUND_HALF_UP)
    
    match XZQArea_path.suffix:
        case ".shp":
            XZQ_gdf = gpd.read_file(XZQArea)
        case "":
            if XZQArea_path.parent.suffix == ".gdb":
                XZQ_gdf = gpd.read_file(XZQArea_path.parent, layer=XZQArea_path.stem)
            else:
                raise ValueError("请输入正确的矢量文件路径")
        case _:
            raise ValueError("请输入正确的矢量文件路径")

    match Area_shp_path.suffix:
        case ".shp":
            Area_gdf = gpd.read_file(XZQArea)
        case "":
            if Area_shp_path.parent.suffix == ".gdb":
                Area_gdf = gpd.read_file(Area_shp_path.parent, layer=Area_shp_path.stem)
            else:
                raise ValueError("请输入正确的矢量文件路径")
        case _:
            raise ValueError("请输入正确的矢量文件路径")
    keylist = XZQ_gdf[XZQ_key].values

    for key in keylist:
        area_sum = compute( XZQ_gdf[XZQ_gdf[XZQ_key] == key][XZQ_area_field].values[0])
        Arealistvalues = Area_gdf[Area_gdf[Area_key] == key][Area_shp_field].values
        Arealist = np.array([compute(v) for v in Arealistvalues])
        Area_average = compute((area_sum - sum(Arealist)) / compute(len(Arealist)))
        Arealist_ = Arealist + Area_average
        if area_sum - sum(Arealist_) == Decimal('0'):
            pass
        
        
