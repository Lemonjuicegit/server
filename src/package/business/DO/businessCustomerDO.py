from sqlmodel import SQLModel
from package.database import TYPE
from datetime import date


class BusinessCustomerDO(SQLModel, table=True):
    __tablename__ = "business_customer"
    id: int = TYPE.PRIMARY_KEY
    name: str  # 客户名称
    taxpayer_no: str  # 纳税人识别号
    address: str  # 地址
    phone: str  # 联系电话
    bank: str  # 开户行
    card_no: str  # 银行卡号
    contact: str  # 联系人
    contact_phone: str  # 联系人电话
    creator: str  # 创建人
    updater: str  # 更新人
    create_time: date  # 创建时间
    update_time: date  # 更新时间
    deleted: int  # 是否删除
    remark: str  # 备注
    nature: int  # 客户性质
    important: int  # 是否要客
