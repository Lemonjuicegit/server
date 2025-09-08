from pathlib import Path
import geopandas as gpd
import os, json

current = Path(os.path.dirname(__file__))
attributetab_path = current / "attributetab.json"
attributetab = json.loads(attributetab_path.read_text(encoding="utf-8"))


def produce_exf(gdbfile, savepath,attformt):
    template_zd = current / "template" / "合川区宗地.exf"
    template_fw = current / "template" / "合川区房屋.exf"
    with open(template_zd, "r", encoding="gb2312") as f:
        zd = f.read().split("\n")
    with open(template_fw, "r", encoding="gb2312") as f:
        fw = f.read().split("\n")
    try:
        gdf_zd = gpd.read_file(gdbfile, layer="宗地")
    except ValueError:
        yield -1, "没有房屋图层"
    try:
        gdf_fw = gpd.read_file(gdbfile, layer="房屋")
    except ValueError:
        yield -1, "没有宗地图层"

    for _, row in gdf_zd.iterrows():
        xy = row.geometry.geoms[0].exterior.xy
        xy_str = "\n".join([f"{x}∴{y}∴100.000000" for x, y in zip(xy[0], xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        FID = row["FID"] if row["FID"] else 0.0
        F_CODE_ID = row["F_CODE_ID"] if row["F_CODE_ID"] else 0.0
        F_TEMP_CODE = row["F_TEMP_CODE"] if row["F_TEMP_CODE"] else ""
        F_TEMP_NAME = row["F_TEMP_NAME"] if row["F_TEMP_NAME"] else ""
        F_PARCEL_NO = row["F_PARCEL_NO"] if row["F_PARCEL_NO"] else ""
        bdcdyh = row["不动产单元代码"] if row["不动产单元代码"] else ""
        F_UNDER_CORNERID = row["F_UNDER_CORNERID"] if row["F_UNDER_CORNERID"] else 0.0
        F_LOC_CORNERID = row["F_LOC_CORNERID"] if row["F_LOC_CORNERID"] else 0.0
        F_LAND_LOC = row["F_LAND_LOC"] if row["F_LAND_LOC"] else ""
        F_CALCULATE_AREA = row["F_CALCULATE_AREA"] if row["F_CALCULATE_AREA"] else 0.0
        F_CREATE_BY = row["F_CREATE_BY"] if row["F_CREATE_BY"] else ""
        F_CREATE_TIME = row["F_CREATE_TIME"] if row["F_CREATE_TIME"] else ""
        F_MODIFY_BY = row["F_MODIFY_BY"] if row["F_MODIFY_BY"] else ""
        F_MODIFY_TIME = row["F_MODIFY_TIME"] if row["F_MODIFY_TIME"] else ""
        F_MODIFY_CIRCS = row["F_MODIFY_CIRCS"] if row["F_MODIFY_CIRCS"] else 0
        F_INDB_RIGHTBY = row["F_INDB_RIGHTBY"] if row["F_INDB_RIGHTBY"] else ""
        F_SERIAL_NO = row["F_SERIAL_NO"] if row["F_SERIAL_NO"] else ""
        F_INDB_USETYPE = row["F_INDB_USETYPE"] if row["F_INDB_USETYPE"] else ""
        F_PARCEL_NUMBER = row["F_PARCEL_NUMBER"] if row["F_PARCEL_NUMBER"] else ""
        F_COMMENT = row["F_COMMENT"] if row["F_COMMENT"] else ""
        F_LOCKED = row["F_LOCKED"] if row["F_LOCKED"] else 0.0
        F_SITE_ID = row["F_SITE_ID"] if row["F_SITE_ID"] else 0
        F_FLY_LAND = row["F_FLY_LAND"] if row["F_FLY_LAND"] else 0
        F_RIGHT_PRO = row["F_RIGHT_PRO"] if row["F_RIGHT_PRO"] else 0
        F_PARCEL_NO_OLD = row["F_PARCEL_NO_OLD"] if row["F_PARCEL_NO_OLD"] else ""
        CODE = row["CODE"] if row["CODE"] else 0

        arr = (
            f"{FID}∴{F_CODE_ID}∴{F_TEMP_CODE}∴{F_TEMP_NAME}∴{F_PARCEL_NO}∴{bdcdyh}∴{F_UNDER_CORNERID}"
            + f"∴{F_LOC_CORNERID}∴{F_LAND_LOC}∴{F_CALCULATE_AREA}∴{F_CREATE_BY}∴{F_CREATE_TIME}∴{F_MODIFY_BY}"
            + f"∴{F_MODIFY_TIME}∴{F_MODIFY_CIRCS}∴{F_INDB_RIGHTBY}∴{F_SERIAL_NO}∴{F_INDB_USETYPE}∴{F_PARCEL_NUMBER}"
            + f"∴{F_COMMENT}∴{F_LOCKED}∴{F_SITE_ID}∴{F_FLY_LAND}∴{F_RIGHT_PRO}∴{F_PARCEL_NO_OLD}∴1∴{CODE}"
        )
        temp1 = "\n".join(zd[:1054])
        temp2 = "\n".join(zd[1054:1094])
        temp3 = "\n".join(zd[1095:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{arr}\n{temp3}"
        with open(
            f"{os.path.join(savepath,f'{bdcdyh}宗地')}.exf", "w", encoding="gbk"
        ) as f:
            f.write(text)
            yield -1, f"{bdcdyh}宗地.exf"
    fields = attributetab["TGEOC_JC_HOUSE_5H"]["fields"]
    hiatus_fiedl = set(fields) - set(gdf_fw)
    if hiatus_fiedl:
        yield -1, f"房屋缺少字段:{list(hiatus_fiedl)}"
    for _, row in gdf_fw.iterrows():
        xy = row.geometry.geoms[0].exterior.xy
        xy_str = "\n".join([f"{x}∴{y}∴100.000000" for x, y in zip(xy[0], xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        arr = ""
        temp = []
        for field in fields:
            if str(row[field]) != "None":
                temp.append(row[field])
            else:
                temp.append("")
        arr = "∴".join([str(v) for v in temp])
        temp1 = "\n".join(fw[:1054])
        temp2 = "\n".join(fw[1054:1106])
        temp3 = "\n".join(fw[1107:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{arr}\n{temp3}"
        bdcdydm = row["不动产单元代码"]
        with open(
            f"{os.path.join(savepath,f'{bdcdydm}房屋')}.exf", "w", encoding="gbk"
        ) as f:
            f.write(text)
            yield -1, f"{row['不动产单元代码']}房屋.exf"

def YB_exf(zdfile,fwfile, savepath):
    template_zd = current / "YB.exf"
    with open(template_zd, "r", encoding="gb2312") as f:
        zd = f.read().split("\n")

    gdf_zd = gpd.read_file(zdfile)
    gdf_fw = gpd.read_file(fwfile)
    for _, row in gdf_zd.iterrows():
        xy = row.geometry.exterior.xy
        xy_str = "\n".join([f"{x}∴{y}∴100.000000" for x, y in zip(xy[0], xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        
        xy_fw = gdf_fw[gdf_fw["ZDDM"] == row["ZDDM"]].loc[0].geometry.exterior.xy
        xy_str_fw = "\n".join(
            [f"{x}∴{y}∴100.000000" for x, y in zip(xy_fw[0], xy_fw[1])]
        )
        xy_str_fw = f"{len(xy[0])}\n{xy_str_fw}"
        ZDDM = row["ZDDM"]
        DJH = row["DJH"]
        BUDCDYH = row["ZDDM"] + 'F0001'
        ZL = "渝北区石船镇葛口村21组1幢1"
        QLR = "黄代均"
        
        arr = f"0.0∴0.0∴112500000∴地表宗地∴{DJH}∴{ZDDM}∴0.0∴0.0∴{ZL}∴75∴余勇∴∴∴∴0∴{QLR}∴∴宅基地∴{ZL}∴∴∴0∴0∴0∴∴1∴112512000"
        fw_arr = f"0.0∴0.0∴∴∴∴∴0.0∴{DJH}∴{BUDCDYH}∴0.0∴0.0∴∴∴∴∴∴∴∴∴∴∴0∴∴∴2∴2110"
        temp1 = "\n".join(zd[:1054])
        temp2 = "\n".join(zd[1054:1067])
        temp3 = "\n".join(zd[1067:1107])
        temp4 = "\n".join(zd[1108:1120])
        temp5 = "\n".join(zd[1121:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{xy_str_fw}\n{temp3}\n{arr}\n{temp4}\n{fw_arr}\n{temp5}"
        with open(
            f"{os.path.join(savepath,f'{ZDDM}{QLR}')}.exf", "w", encoding="gbk"
        ) as f:
            f.write(text)
            
            
if __name__ == '__main__':
    zdfile = r"C:\Users\Administrator\Desktop\渝北修改\石船\500112009011JC02510\宗地.shp" 
    fwfile = r"C:\Users\Administrator\Desktop\渝北修改\石船\500112009011JC02510\房屋.shp"
    savepath = r"C:\Users\Administrator\Desktop\渝北修改\石船\500112009011JC02510"
    YB_exf(zdfile, fwfile, savepath)