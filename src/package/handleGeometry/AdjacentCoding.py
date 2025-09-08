import geopandas as gpd
from package.utils import groupby
from shapely import MultiLineString, Point

def AdjacentCoding(shp, fiedl_key, precision=0):
    """通过线的端点检查相邻线编码是否重复(排除三交以上的点)

    Args:
        shp (GeoDataFrame)
        savapath (Path | str)
    """
    resdf = gpd.GeoDataFrame(columns=["fiedl_key", "x", "y", "add","keyadd", "geometry"])
    for _, row in shp.iterrows():
        if isinstance(row.geometry, MultiLineString):
            point_xy = row.geometry.geoms[0].xy
        else:
            point_xy = row.geometry.xy
        po1 = Point(point_xy[0][0], point_xy[1][0])
        po2 = Point(point_xy[0][-1], point_xy[1][-1])
        resdf.loc[resdf.shape[0]] = [
            row[fiedl_key],
            point_xy[0][0],
            point_xy[1][0],
            f"{str(point_xy[0][0])[:-1-precision]}{str(point_xy[1][0])[:-1-precision]}",
            f"{row[fiedl_key]}{point_xy[0][0]}{point_xy[1][0]}",
            po1,
        ]
        resdf.loc[resdf.shape[0]] = [
            row[fiedl_key],
            point_xy[0][-1],
            point_xy[1][-1],
            f"{point_xy[0][-1]}{point_xy[1][-1]}",
            f"{row[fiedl_key]}{point_xy[0][-1]}{point_xy[1][-1]}",
            po2,
        ]
    resdf_by = groupby(resdf, ["add"], "count")
    resdf_screen = resdf_by[resdf_by['COUNT'] == 2]
    resdf_by = groupby(resdf_screen.drop('COUNT',axis=1), ["keyadd"], "count")
    res = resdf_by[resdf_by['COUNT'] == 2]
    res = res[~res["fiedl_key"].isnull()]
    res.crs = shp.crs
    return res