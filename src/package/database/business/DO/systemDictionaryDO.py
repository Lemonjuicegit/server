from sqlmodel import SQLModel, Relationship
from package.database.TYPE import TYPE
from datetime import date


class SystemDictionaryDO(SQLModel, table=True):
    __tablename__ = "system_dictionary"
    id: int = TYPE.PRIMARY_KEY
    parent_id: int  # 父ID
    label: str  # 字典标签
    sort: int  # 顺序
    remark: str  # 备注
    color_type: str  # 字典类型
    css_class: str  # CSS Class
    dept_analyse: int  # 核算到部门
    project_analyse: int  # 核算到项目
    status: int  # 状态
    creator: str  # 创建人
    updater: str  # 最后更新人
    create_time: date  # 创建时间
    update_time: date  # 最后更新时间
    deleted: int  # 是否删除
    value: str  # 字典键值
    cost_type: str  # 成本类型
