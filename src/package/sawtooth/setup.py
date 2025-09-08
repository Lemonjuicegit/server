from math import sqrt,acos,degrees
import geopandas as gpd
from shapely import Polygon,MultiPolygon,LineString

record = r''
f = open(record,'a',encoding='gb2312')
def haversine(a,b,c)->float|0:
    """
    根据三个点的坐标计算向量夹角的度数。

    Args:
    a,b,c -- 三个点的坐标，每个点是一个包含x和y坐标的元组。

    return:
    夹角的度数，如果没有有效夹角则返回0。
    """
    # 计算向量内积
    ab_bc = (b[0]-a[0])*(c[0]-b[0]) + (b[1]-a[1])*(c[1]-b[1])
    # 计算模
    ab = sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)
    bc = sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2)
    # 计算夹角
    if ab * bc == 0:
        return 0
    cosA = ab_bc / (ab * bc)
    if -1 < cosA < 1:
        theta = acos(ab_bc / (ab * bc))
        return degrees(theta)
    return 0

def sawtooth_xy(xy,por,ignore:int)->{list,int}:
    """
    根据给定的点序列和多边形，过滤出外边界点。

    Args:
    xy -- 点序列，每个点是一个包含x和y坐标的元组。
    por -- 多边形对象。
    ignore -- 忽略的点的数量，用于处理多边形的起始和结束点。

    return:
    过滤后的外边界点序列和一个标志位。
    """
    outer_coords = []
    if len(xy) <= ignore:
        return xy,1
    for index,value in enumerate(xy):
        if index == 0:
            front = xy[len(xy)-1]
        else:
            front = xy[index-1]
        mid = value
        if index == len(xy)-1:
            back = xy[0]
        else:
            back = xy[index+1]
        if 89.9 <= haversine(front,mid,back) <= 90.1:
            lin = gpd.GeoSeries(LineString([front,back]))
            if lin.within(por).values[0]:
                outer_coords.append(mid)
        else:
            outer_coords.append(mid)

    return outer_coords,0

def sawtooth_pol(por,tbbh)->Polygon:
    """
    处理多边形的外边界和内边界，生成一个新的多边形。
    
    Args:
    por -- 多边形对象。
    tbbh -- 多边形的标识符。

    return:
    新的多边形对象，其边界点经过sawtooth算法处理。
    """
    inner_coords = []
    xy = list(zip(por.exterior.xy[0],por.exterior.xy[1]))
    outer_coords,wbj = sawtooth_xy(xy,por,15)
    if wbj:
        f.write(f"{tbbh}:外边界")
    if por.interiors:
        for lin in por.interiors :
            interiors_xy =  list(zip(lin.xy[0],lin.xy[1]))
            inner,nbj = sawtooth_xy(interiors_xy,por,10)
            inner_coords.append(inner)
            if nbj:
                f.write(f"{tbbh}:内边界")
    if inner_coords:
        return Polygon(outer_coords,inner_coords)

    return Polygon(outer_coords)
             
def sawtooth(shppath,save):
    """
    读取shapefile文件，对其中的多边形进行sawtooth处理，并保存结果。
    
    Args:
    shppath -- shapefile文件的路径。
    save -- 处理后的shapefile文件保存路径。
    """
    gdf = gpd.read_file(shppath)
    sawtooth_gdf = gpd.GeoDataFrame(columns=gdf.columns)

    for _,row in gdf.iterrows():
        if isinstance(row.geometry,MultiPolygon):
            por = row.geometry.geoms[0]
        else:
            por = row.geometry
        sawtooth_gdf.loc[sawtooth_gdf.shape[0]] = [*row[:-1],Polygon(sawtooth_pol(por,row.tbbh))]
        yield f"{row.tbbh}完成"
    f.close()
    sawtooth_gdf.to_file(save,encoding="gb18030")

if __name__ == '__main__':
    shp = r"E:\工作文档\开州项目\后备资源.shp"
    savepath = r"E:\工作文档\开州项目\新建文件夹\后备资源.shp"
    res = sawtooth(shp,savepath)
    for v in res:
        print(v)
