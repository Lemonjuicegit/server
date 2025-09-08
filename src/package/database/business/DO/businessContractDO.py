from sqlmodel import SQLModel
from package.database import TYPE
from datetime import date
from typing import List


class BusinessContractDO(SQLModel, table=True):
    __tablename__ = "business_contract"
    id: int = TYPE.PRIMARY_KEY
    name: str  # 合同名称
    code: str  # 合同编号
    signing_company: str  # 签约主体(乙方)
    signing_company_list: str
    nature: int  # 合同性质
    type: int  # 合同类别
    customer_addr: str  # 客户联系地址
    begin_date: date  # 合同开始日期
    end_date: date  # 合同结束日期
    amount: float  # 合同金额
    draft_user: int  # 合同制定人
    sign_user: int  # 合同签订人
    sign_date: date  # 合同签订时间
    sign_dept: int  # 合同签订部门
    save_user: int  # 合同保管人
    iid: int  # 业务编号
    notes: str  # 备注
    customer_name: str  # 客户名称(甲方)
    customer_representative: str  # 签约客户代表
    customer_tel: str  # 客户联系电话
    status: int  # 合同状态，有效失效
    dept_id: int  # 部门ID
    creator: str  # 创建人
    create_time: date  # 创建时间
    update_time: date  # 更新时间
    updater: str  # 更新人
    deleted: int  # 是否删除
    estimated_sign_date: date  # 预计签订时间
    original_quantity: int  # 原件份数
    follower: int  # 合同跟进人
    follower_name: str  # 合同跟进人
    achieve_status: int  # 归档状态
    achiever: int  # 归档人
    achiever_name: str  # 归档人
    achieve_date: date  # 归档时间
    process_instance_id: str  #
    result: str  #
    statistics_time: date  # 合同统计时间
    responsible_person: str  # 合同责任人
    customer_name_list: int
    signing_company_list: int
