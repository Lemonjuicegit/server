from pathlib import Path
import geopandas as gpd

field = ['FID','F_CODE_ID','F_TEMP_CODE','F_TEMP_NAME','F_UNDER_CORNERID','F_OBJECT_NAME','F_PARCEL_ID','F_UNDER_PARCEL_NO','不动产单元号','F_BASE_AREA','F_CALCULATE_AREA','F_CREATE_BY','F_CREATE_TIME','F_MODIFY_BY','F_MODIFY_TIME','F_SERIAL_NO','F_BUILDING_TYPE','F_BUILDING_STOREY','F_BUILDING_NO','F_COMMENT','F_LOCKED','F_SITE_ID','F_BLOCK','F_BUILDING_NO_OLD','ID','CODE']
 
 
gdf = gpd.read_file(r'E:\工作文档\其他\合川\合川区.gdb',layer='房屋修改补录')

pass

gdf.columus