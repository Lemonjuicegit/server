"""
arcgis属性表值对比
"""

import geopandas as gpd
import pandas as pd
from package.handleGeometry.utils import read_gdf, exact_round


def attributeEquals(shp1, shp2, key_field, precision):
    gdf1 = read_gdf(shp1)
    gdf2 = read_gdf(shp2)
    res_df = pd.DataFrame(columns=[*gdf1.columns[:-2],'key'])

    def rowEq(row):
        eq_df = (
            gdf2[gdf2["shape_Length"] == row["shape_Length"]]
            .copy()
        )
        if eq_df.shape[0]:

            eq = row == eq_df.reset_index(drop=True).loc[0]

            res_df.loc[res_df.shape[0]] = [*list(eq)[:-2], row[key_field]]

    gdf1.apply(rowEq, axis=1)
    return res_df
