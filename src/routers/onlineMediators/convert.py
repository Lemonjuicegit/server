from datetime import datetime
from typing import Union, Optional, Dict, Any
from sqlmodel import SQLModel
from src.package.重庆市网上中介服务信息.DO.cgggDO import CgggDO


def convert_cggg_datetime_to_string(DO: SQLModel) -> Dict[str, Any]:
    """
    将CgggDO模型中的datetime类型字段转换为字符串，并将空值也转为字符串
    
    Args:
        cggg_item: CgggDO实例或字典对象
        
    Returns:
        转换后的字典，其中datetime字段已转换为字符串格式，空值转为空字符串
    """
    # 如果输入是CgggDO实例，则转换为字典

    result = DO.model_dump()
    
    # 处理其他可能的空值字段
    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        if value is None:
            result[key] = ""
    
    return result


def convert_list(DO_list: list[SQLModel]) -> list:
    """
    批量转换CgggDO列表中的datetime类型字段为字符串
    
    Args:
        cggg_list: 包含CgggDO实例或字典的列表
        
    Returns:
        转换后的字典列表
    """
    return [convert_cggg_datetime_to_string(item) for item in DO_list]