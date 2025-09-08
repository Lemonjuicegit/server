import geopandas as gpd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

def read_gdf(datapath,crs):
    vector = Path(datapath)
    match vector.suffix:
        case ".shp":
            gdf = gpd.read_file(vector)
        case "":
            if vector.parent.suffix == ".gdb":
                gdf = gpd.read_file(vector.parent, layer=vector.stem)
            else:
                raise ValueError("请输入正确的矢量文件路径")
        case _:
            raise ValueError("请输入正确的矢量文件路径")
    gdf = gdf.to_crs(crs)
    return gdf

def exact_round(x:int| float, precision:int):
    return Decimal(x).quantize(Decimal(f"0.{'0'*precision}"), ROUND_HALF_UP)

def to_geojson(filepath, crs):
    gdf = read_gdf(filepath,crs)
    return gdf.to_json(na='null',show_bbox=True,drop_id=True)

if __name__ == '__main__':
    testdata = r"E:\工作文档\测试导出数据\新增耕地范围.shp"
    res = read_gdf(testdata, 3857)
    pass