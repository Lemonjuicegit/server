from pathlib import Path
import geopandas as gpd
import os, json
from .. import state

current = Path(os.path.dirname(__file__))
attributetab_path = current / "attributetab.json"
attributetab = json.loads(attributetab_path.read_text(encoding="utf-8"))

def hc_exf(gdbfile, savepath):
    """
    从给定的GDB文件中导出宗地和房屋数据，并根据模板生成相应的EXF文件。

    Args:
    gdbfile (str): GDB文件的路径。
    savepath (str): 生成的EXF文件保存的路径。

    return:
    state.ERR (str): 当发生错误时，生成错误信息。
    state.RES (str): 当成功生成EXF文件时，生成成功信息。
    """
    template_zd = current / "template" / "宗地模板.exf"
    template_fw = current / "template" / "房屋模板.exf"
    with open(template_zd, "r", encoding="gb2312") as f:
        zd = f.read().split("\n")
    with open(template_fw, "r", encoding="gb2312") as f:
        fw = f.read().split("\n")
    try:
        gdf_zd = gpd.read_file(gdbfile, layer="宗地")
    except ValueError:
        yield state.ERR, "没有房屋图层"
    try:
        gdf_fw = gpd.read_file(gdbfile, layer="房屋")
    except ValueError:
        yield state.ERR, "没有宗地图层"

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
            yield state.RES, f"{bdcdyh}宗地.exf"
    fields = attributetab["TGEOC_JC_HOUSE_5H"]["fields"]
    hiatus_fiedl = set(fields) - set(gdf_fw)
    if hiatus_fiedl:
        yield state.ERR, f"房屋缺少字段:{list(hiatus_fiedl)}"
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
            yield state.RES, f"{row['不动产单元代码']}房屋.exf"


def lq_exf(gdbpath, savepath):
    """
    从给定的GDB路径读取林权数据并保存为EXF格式文件。

    该函数读取预定义模板文件“林权.exf”，然后尝试从给定的GDB路径中读取“宗地”图层。
    它检查是否存在所有必需的字段，并为“宗地”图层中的每一项生成一个EXF文件。

    Args:
    gdbpath (str): GDB文件的路径。
    savepath (str): 保存生成的EXF文件的路径。

    return:
    tuple: (状态码, 消息)
        - 当生成EXF文件时，生成一个包含成功消息的元组。
        - 如果发生错误，生成一个包含错误消息的元组。
    """
    with open(current / "template" / "林权.exf", "r", encoding="gb2312") as f:
        zd = f.read().split("\n")
    try:
        gdf_zd = gpd.read_file(gdbpath, layer="宗地")
    except ValueError:
        yield state.ERR, "没有宗地图层"

    fields = attributetab["TGEOC_DJ_PARCEL_5H"]["fields"]
    if fields - set(gdf_zd.columns):
        yield state.ERR, f"缺少字段:{fields - set(gdf_zd.columns)}"
    for _, row in gdf_zd.iterrows():
        xy = row.geometry.geoms[0].exterior.xy
        xy_str = "\n".join([f"{x}∴{y}∴0.000000" for x, y in zip(xy[0], xy[1])])
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
            f"{os.path.join(savepath,f'{bdcdyh}宗地')}.exf", "w", encoding="gb2312"
        ) as f:
            f.write(text)
            yield state.RES, f"{bdcdyh}宗地.exf"


def yb_exf(gdbpath, fwgdb, savepath):
    
    """
    根据给定的地理数据库路径、辅助图形数据库路径和保存路径，
    生成并保存宗地的电子交换文件。

    Args:
    gdbpath (str): 地理数据库路径。
    fwgdb (str): 辅助图形数据库路径。
    savepath (str): 保存电子交换文件的路径。
    """
    with open(current / "template" / "模板.exf", "r", encoding="gb2312") as f:
        zd = f.read().split("\n")

    gdf_zd = gpd.read_file(gdbpath)

    gdf_fw = gpd.read_file(fwgdb)
    attributetab_path = current / "attributetab.json"
    with open(attributetab_path, "r", encoding="utf-8") as f:
        fields = set(json.loads(f.read())["TGEOC_DJ_PARCEL_5H"]["fields"])
    for _, row in gdf_zd.iterrows():
        xy = row.geometry.exterior.xy
        xy_fw = gdf_fw.geometry.loc[0].exterior.xy
        xy_str = "\n".join([f"{x}∴{y}∴0.000000" for x, y in zip(xy[0], xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        xy_fw = '\n'.join([f'{x}∴{y}∴0.000000' for x,y in zip(xy_fw[0],xy_fw[1])])
        xy_fw = f"{len(xy_fw[0])}\n{xy_fw}"
        F_CODE_ID = row['F_CODE_ID'] if row['F_CODE_ID'] else 0.0
        F_TEMP_CODE = row['F_TEMP_CODE'] if row['F_TEMP_CODE'] else ''
        F_TEMP_NAME = row['F_TEMP_NAME'] if row['F_TEMP_NAME'] else ''
        F_PARCEL_NO = row['DJH']
        ZDDM = row["ZDDM"]
        F_UNDER_CORNERID = row['F_UNDER_CORNERID'] if row['F_UNDER_CORNERID'] else 0.0
        F_LOC_CORNERID = row['F_LOC_CORNERID'] if row['F_LOC_CORNERID'] else 0.0
        F_LAND_LOC = row['ZL']
        F_CALCULATE_AREA = row['ZDMJ']
        F_CREATE_BY = row['F_CREATE_BY'] if row['F_CREATE_BY'] else ''
        F_CREATE_TIME = row['F_CREATE_TIME'] if row['F_CREATE_TIME'] else ''
        F_MODIFY_BY = row['F_MODIFY_BY'] if row['F_MODIFY_BY'] else ''
        F_MODIFY_TIME = row['F_MODIFY_TIME'] if row['F_MODIFY_TIME'] else ''
        F_MODIFY_CIRCS = row['F_MODIFY_CIRCS'] if row['F_MODIFY_CIRCS'] else 0
        F_INDB_RIGHTBY = row['F_INDB_RIGHTBY'] if row['F_INDB_RIGHTBY'] else ''
        F_SERIAL_NO = row['F_SERIAL_NO'] if row['F_SERIAL_NO'] else ''
        F_INDB_USETYPE = row['F_INDB_USETYPE'] if row['F_INDB_USETYPE'] else ''
        F_PARCEL_NUMBER = row['F_PARCEL_NUMBER'] if row['F_PARCEL_NUMBER'] else ''
        F_COMMENT = row['F_COMMENT'] if row['F_COMMENT'] else ''
        F_LOCKED = row['F_LOCKED'] if row['F_LOCKED'] else 0.0
        F_SITE_ID = row['F_SITE_ID'] if row['F_SITE_ID'] else 0
        F_FLY_LAND = row['F_FLY_LAND'] if row['F_FLY_LAND'] else 0
        F_RIGHT_PRO = row['F_RIGHT_PRO'] if row['F_RIGHT_PRO'] else 0
        F_PARCEL_NO_OLD = row['F_PARCEL_NO_OLD'] if row['F_PARCEL_NO_OLD'] else ''
        CODE = row['CODE'] if row['CODE'] else 0

        arr = f"0.0∴0.0∴112500000∴地表宗地∴{F_PARCEL_NO}∴{ZDDM}∴0.0" + \
            f"∴0.0∴{F_LAND_LOC}∴{F_CALCULATE_AREA}∴**∴∴" + \
            f"∴0∴**∴{F_INDB_RIGHTBY}∴{F_SERIAL_NO}∴{F_INDB_USETYPE}∴{F_PARCEL_NUMBER}" + \
            f"∴{F_COMMENT}∴{F_LOCKED}∴{F_SITE_ID}∴{F_FLY_LAND}∴{F_RIGHT_PRO}∴{F_PARCEL_NO_OLD}∴1∴{CODE}"
        temp1 = "\n".join(zd[:1054])
        temp2 = "\n".join(zd[1054:1067])
        temp3 = "\n".join(zd[1067:1094])
        temp4 = "\n".join(zd[1095:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{xy_str}\n{temp3}\n{temp4}"
        with open(
            f"{os.path.join(savepath,f'{ZDDM}宗地')}.exf", "w", encoding="gb2312"
        ) as f:
            f.write(text)


if __name__ == "__main__":
    shp = r"E:\工作文档\测试导出数据\合川3.11\钓鱼城街道.gdb"
    template_zd = r"E:\exploitation\webpython\routers\hc\合川区+宗地+20220517（南屏农机加油站）.exf"
    template_fw = (
        r"E:\exploitation\webpython\routers\hc\合川区+房屋（XX车库）+中间库.exf"
    )
    savepath = r"E:\工作文档\测试导出数据\合川"
    hc_exf(shp, savepath)

    # gdb = r"E:\工作文档\其他\处理胡建国坐宗坐标纠正\500112144206JC00007胡建国.shp"
    # yb_exf(gdb,gdb,r'E:\工作文档\其他\处理胡建国坐宗坐标纠正')
