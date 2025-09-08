import math
import geopandas as gpd
from pathlib import Path
from shapely import Point, Polygon, MultiPolygon


class gardens:
    def __init__(self, jd, shppath, templaet) -> None:
        """
        处理园林数据的类，用于读取、处理和保存园林相关的地理数据。
        
        Args:
        - jd: 保存处理后的经纬度数据的文件路径。
        - shppath: 包含园林地理信息的shp文件路径。
        - templaet: 用于处理数据的模板文件路径。
        """
        self.gdf = gpd.read_file(shppath)
        self.temp_path = Path(templaet)
        self.temp = self.temp_path.read_text(encoding="gb2312").rpartition("\n")
        self.temp_head = self.temp[0]
        self.temp = self.temp[2].split(",")

        def filter_key(item):
            if len(item) > 0:
                if item[0] == "#":
                    return item

        self.key_field = list(filter(filter_key, self.temp))[0][1:]
        self.getJd(jd)
        self.delgdf = gpd.GeoDataFrame(columns=["dkh", "geometry"], crs=self.gdf.crs)

    def getJd(self, save):
        """
        处理经纬度数据并保存到文件。
        
        Args:
        - save: 保存处理后数据的文件路径。
        """
        self.jd = gpd.GeoDataFrame(
            columns=["dkh", "xh", "JZDH", "geometry"], crs=self.gdf.crs
        )

        def coordinate(row):
            if type(row.geometry) == MultiPolygon:
                por = row.geometry.geoms[0]
            else:
                por = row.geometry
            xy = list(zip(por.exterior.xy[0], por.exterior.xy[1]))
            n = 1
            for i in xy:
                if n == len(xy):
                    self.jd.loc[self.jd.shape[0]] = [
                        row[self.key_field],
                        "1",
                        "J1",
                        Point(i[0], i[1]),
                    ]
                else:
                    self.jd.loc[self.jd.shape[0]] = [
                        row[self.key_field],
                        "1",
                        f"J{n}",
                        Point(i[0], i[1]),
                    ]
                    n += 1
            max_n = n
            if por.interiors:
                xh = 2
                for lin in por.interiors:
                    interiors_xy = list(zip(lin.xy[0], lin.xy[1]))
                    for i in interiors_xy:
                        if (n - max_n + 1) == len(interiors_xy):
                            self.jd.loc[self.jd.shape[0]] = [
                                row[self.key_field],
                                str(xh),
                                f"J{max_n}",
                                Point(i[0], i[1]),
                            ]
                        else:
                            self.jd.loc[self.jd.shape[0]] = [
                                row[self.key_field],
                                str(xh),
                                f"J{n}",
                                Point(i[0], i[1]),
                            ]
                        n += 1
                    xh += 1

        self.gdf.apply(coordinate, axis=1)
        self.jd.to_file(save, encoding="gb18030")

    def delJd(self, accuracy, field, save):
        """
        根据精度删除多余的顶点。
        
        Args:
        - accuracy: 顶点间的最小距离，用于决定是否删除顶点。
        - field: 用于标识的字段名。
        - save: 保存处理后数据的文件路径。
        """
        def shan(row):
            sxy = [0, 0]
            xy = list(zip(row.geometry.exterior.xy[0], row.geometry.exterior.xy[1]))
            n = 0
            catXY = []
            for i in xy:
                if sxy[0]:
                    lenth = math.sqrt((sxy[0] - i[0]) ** 2 + (sxy[1] - i[1]) ** 2)
                    if lenth > accuracy:
                        catXY.append((i[0], i[1]))
                else:
                    catXY.append((i[0], i[1]))
                sxy[0] = i[0]
                sxy[1] = i[1]
                n += 1
            self.delgdf.loc[self.delgdf.shape[0]] = [row[field], Polygon(catXY)]

        self.gdf.apply(shan, axis=1)
        self.delgdf["geometry"] = self.delgdf["geometry"].apply(
            lambda geom: geom.zxy if geom.has_z else geom
        )
        self.delgdf.to_file(save, encoding="gb18030")

    def get_coordinate_string(self, save, ndigits=2):
        """
        生成并保存坐标字符串。
        
        Args:
        - save: 保存生成字符串的文件路径。
        - ndigits: 保存小数点后的位数，默认为2。
        """
        with open(save, "a", encoding="gb2312") as f:
            f.write(f"{self.temp_head}\n")

            def coordinate(row):
                dkh = row[self.key_field]
                por = self.jd[self.jd["dkh"] == dkh]
                att = ""
                for t in self.temp:
                    if len(t) > 0:
                        if t[0] in ["$", "#"]:
                            att = f"{att},{row[t[1:]]}" if att else row[t[1:]]
                            continue
                        if t == "&index":
                            att = f"{att},{len(por)-1}" if att else str(len(por) - 1)
                            continue
                        att = f"{att},{t}" if att else t
                    else:
                        att = f"{att}," if att else t
                att = f"{att}\n"
                f.write(att)
                for _, item in por.iterrows():
                    f.write(
                        f"{item.JZDH},{item.xh},{round(item.geometry.y,ndigits)},{round(item.geometry.x,ndigits)}\n"
                    )

            self.gdf.apply(coordinate, axis=1)


def readData(path, save):
    with open(path, "r", encoding="gb2312") as f:
        text = f.read().split("\n")
    n = 0
    gdf = gpd.GeoDataFrame(columns=("MJ", "QLR", "DJH", "geometry"))
    zb = []
    while n < len(text):
        temp = text[n].split(",")
        if temp[0][0] == "J":
            zb.append([float(temp[3]), float(temp[2])])
            n += 1
        else:
            if zb:
                temp2 = text[n - len(zb) - 1].split(",")
                gdf.loc[gdf.shape[0]] = [temp2[1], temp2[3], temp2[5], Polygon(zb)]
                zb = []
            n += 1

    gdf.to_file(save, encoding="gb18030")


if __name__ == "__main__":
    path_ = r"E:\工作文档\测试导出数据\1008"
    jd = rf"{path_}\jd.shp"
    shp = rf"{path_}\万古27导坐标192块.shp"
    temp = rf"{path_}\新增模板.txt"
    save = rf"{path_}\万古27导坐标192块.txt"
    gar = gardens(jd, shp, temp)
    # gar.delJd(0.1,'DKBH',fr'{path_}\删除点.shp')
    gar.get_coordinate_string(save, 3)
