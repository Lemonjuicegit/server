import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point, Polygon, MultiPolygon
import math


class Gardens:
    def __init__(self, shp_path, template_path):
        self.gdf = gpd.read_file(shp_path)
        self.template_path = template_path
        self._parse_template()
        self._initialize_dataframes()

    def _parse_template(self):
        # 解析模板文件
        content = self.template_path.read_text(encoding="gb2312").rpartition("\n")
        self.template_header, _, self.template_body = content
        self.template_body = [line.strip() for line in self.template_body.split(",")]
        self.key_field = next(
            (line[1:] for line in self.template_body if line.startswith("#")), ""
        )

    def _initialize_dataframes(self):
        # 初始化数据框
        self.jd = gpd.GeoDataFrame(
            columns=["dkh", "xh", "JZDH", "geometry"], crs=self.gdf.crs
        )
        self.delgdf = gpd.GeoDataFrame(columns=["dkh", "geometry"], crs=self.gdf.crs)

    def extract_coordinates(self, save_path):
        # 提取坐标点
        def process_geometry(row):
            geometry = row.geometry
            if isinstance(geometry, MultiPolygon):
                polygons = geometry.geoms
            else:
                polygons = [geometry]

            for polygon in polygons:
                exterior_coords = polygon.exterior.coords
                interior_coords = polygon.interiors

                for xh, coords in enumerate(
                    [exterior_coords] + interior_coords, start=1
                ):
                    for idx, coord in enumerate(coords):
                        label = f"J{idx+1}"
                        if idx == len(coords) - 1 and xh > 1:
                            label = f"J{len(exterior_coords)}"
                        self.jd.loc[len(self.jd)] = [
                            row[self.key_field],
                            str(xh),
                            label,
                            Point(coord),
                        ]

        self.gdf.apply(process_geometry, axis=1)
        self.jd.to_file(save_path, encoding="gb18030")

    def simplify_geometry(self, accuracy, field, save_path):
        # 简化几何图形
        def simplify_polygon(row):
            exterior_coords = row.geometry.exterior.coords
            simplified_coords = [exterior_coords[0]]

            for prev, curr in zip(exterior_coords, exterior_coords[1:]):
                distance = math.sqrt(
                    (prev[0] - curr[0]) ** 2 + (prev[1] - curr[1]) ** 2
                )
                if distance > accuracy:
                    simplified_coords.append(curr)

            simplified_polygon = Polygon(simplified_coords)
            self.delgdf.loc[len(self.delgdf)] = [row[field], simplified_polygon]

        self.gdf.apply(simplify_polygon, axis=1)
        self.delgdf.to_file(save_path, encoding="gb18030")

    def generate_coordinate_string(self, save_path, precision):
        # 生成坐标字符串
        with open(save_path, "w", encoding="gb2312") as file:
            file.write(f"{self.template_header}\n")

            def write_coordinates(row):
                attributes = ",".join(
                    str(row[col[1:]])
                    for col in self.template_body
                    if col.startswith(("$", "#"))
                )
                attributes += (
                    f",{len(self.jd[self.jd['dkh'] == row[self.key_field]])-1}\n"
                )
                file.write(attributes)

                for _, item in self.jd[
                    self.jd["dkh"] == row[self.key_field]
                ].iterrows():
                    file.write(
                        f"{item.JZDH},{item.xh},{round(item.geometry.y, precision)},{round(item.geometry.x, precision)}\n"
                    )

            self.gdf.apply(write_coordinates, axis=1)


def read_data(input_path, output_path):
    with open(input_path, "r", encoding="gb2312") as file:
        lines = file.readlines()

    gdf = gpd.GeoDataFrame(columns=("MJ", "QLR", "DJH", "geometry"))
    current_polygon = []

    for line in lines:
        parts = line.strip().split(",")
        if parts[0].startswith("J"):
            current_polygon.append((float(parts[3]), float(parts[2])))
        else:
            if current_polygon:
                polygon = Polygon(current_polygon)
                gdf.loc[len(gdf)] = [parts[1], parts[3], parts[5], polygon]
                current_polygon = []

    gdf.to_file(output_path, encoding="gb18030")
