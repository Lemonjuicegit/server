def Degree(d=0, f=0, m=0):
    # 度分秒转度
    return d + f / 60 + m / 3600


def sec(d=0, f=0, m=0):
    # 度分秒转秒
    return d * 3600 + f * 60 + m


def degrees_to_dms(degrees):
    d = int(degrees)
    minutes_t = (degrees - d) * 60
    m = int(minutes_t)
    s = (minutes_t - m) * 60
    return [d, m, s]


def HTBH_W(latitude, longitude):
    """一万比例尺的HTBH

    Args:
        latitude (list): 经度
        longitude (list): 纬度

    Returns:
        _type_: str
    """
    million_latitude = [chr(i) for i in range(65, 91)]
    million_row = million_latitude[int(longitude[0] / 4)]
    million_col = int(latitude[0] / 6) + 1
    wd = sec(*longitude)  # 纬度十进制值
    jd = sec(*latitude)  # 经度十进制值
    w_row = str(int((wd - int(wd / 14400) * 14400) / 150) + 1)
    w_col = str(int((jd - int(jd / 21600) * 21600) / 225) + 1)
    row_h = "0" * (3 - len(w_row))
    col_h = "0" * (3 - len(w_col))
    return f"{million_row}{million_col}G{row_h}{w_row}{col_h}{w_col}"


if __name__ == "__main__":
    # 110018.55503 | 390455.74225
    xy1 = [
        [108, 27, 35.74225],
        [30, 33, 38.55503],
    ]
    # 109877.94826 | 390472.13273
    xy2 = [
        [108, 27, 52.13273],
        [30, 31, 17.94826],
    ]
    # w_row1 = str(int((390455.74225 - int(390455.74225 / 14400) * 14400) / 150) + 1)
    # w_row2 = str(int((390472.13273 - int(390472.13273 / 14400) * 14400) / 150) + 1)
    res = HTBH_W(*xy1)
    # print(w_row1, w_row2)
    print(res)
