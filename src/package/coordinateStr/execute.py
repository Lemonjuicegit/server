import math, os
import geopandas as gpd
from pathlib import Path
from shapely import Point, Polygon, MultiPolygon


class gardens:
    def __init__(self, jd, shppath, templaet: Path) -> None:
        self.gdf = gpd.read_file(shppath)
        self.temp_path = templaet
        self.temp = self.temp_path.read_text(encoding="gb2312").rpartition("\n")
        self.temp_head = self.temp[0]
        self.temp = self.temp[2].split(",")
        def filter_key(item):
            if len(item) > 0:
                if item[0] == "#":
                    return item
        self.key_field = list(filter(filter_key, self.temp))[0][1:]
        if os.path.exists(jd):
            self.jd = gpd.read_file(jd)
        else:
            self.getJd(jd)
        self.delgdf = gpd.GeoDataFrame(
            columns=["dkh", "xh", "JZDH", "geometry"], crs=self.gdf.crs
        )

    def getJd(self, save):
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

    def delJd(self, accuracy, key_field, save):
        key_list = set(self.jd[key_field].values)

        for i in key_list:
            jddata = self.jd[self.jd[key_field] == i]
            sxy = [0, 0]
            for _, row in jddata.iterrows():
                x = row.geometry.x
                y = row.geometry.y
                if sxy[0]:
                    lenth = math.sqrt((sxy[0] - x) ** 2 + (sxy[1] - y) ** 2)
                    if lenth > accuracy:
                        self.delgdf.loc[self.delgdf.shape[0]] = [
                            *list(row)[:-1],
                            Point(x, y),
                        ]
                sxy[0] = x
                sxy[1] = y

        self.delgdf.to_file(save, encoding="gb18030")

    def get_coordinate_string(self, save, precision):
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
                            att = f"{att},{len(por) - 1}" if att else str(len(por) - 1)
                            continue
                        att = f"{att},{t}" if att else t
                    else:
                        att = f"{att}," if att else t
                att = f"{att}\n"
                f.write(att)
                for _, item in por.iterrows():
                    f.write(
                        f"{item.JZDH},{item.xh},{round(item.geometry.y, precision)},{round(item.geometry.x, precision)}\n"
                    )

            self.gdf.apply(coordinate, axis=1)
            return save


def jd_to_pol(data, field, xh_field, key_field, save):
    gpdjd = gpd.read_file(data)
    gpfplo = gpd.GeoDataFrame(columns=[*field, "geometry"], crs=gpdjd.crs)
    key = set(gpdjd[key_field].values)
    for i in key:
        holes = []
        poly = gpdjd[gpdjd[key_field] == i]
        xh_list = list(set(poly[xh_field].tolist()))
        x_list = poly[poly[xh_field] == "1"]["geometry"].x.tolist()
        y_list = poly[poly[xh_field] == "1"]["geometry"].y.tolist()
        xy_list = list(zip(x_list, y_list))
        if len(xh_list) > 1:
            for xh in xh_list[1:]:
                holes_x = poly[poly[xh_field] == xh]["geometry"].x.tolist()
                holes_y = poly[poly[xh_field] == xh]["geometry"].y.tolist()
                holes.append(list(zip(holes_x, holes_y)))
            gpfplo.loc[gpfplo.shape[0]] = [i, Polygon(xy_list, holes=holes)]
        else:
            gpfplo.loc[gpfplo.shape[0]] = [i, Polygon(xy_list)]
    gpfplo.to_file(save, encoding="gb18030")


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
    savepath = r"E:\工作文档\测试导出数据\1022"
    shpname = "万古27导坐标最终"
    gar = gardens(
        rf"{savepath}\节点.shp",
        rf"{savepath}\{shpname}.shp",
        Path(rf"{savepath}\新增模板(2).txt"),
    )
    gar.get_coordinate_string(rf"{savepath}\{shpname}.txt", 3)
