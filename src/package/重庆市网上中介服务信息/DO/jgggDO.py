from sqlmodel import SQLModel
from datetime import date,datetime
from src.package.database import TYPE
from typing import Optional
import uuid


class JgggDO(SQLModel,table=True):
    __tablename__ = "jggg"
    id: uuid.UUID = TYPE.PRIMARY_KEY
    #项目名称
    project_name: Optional[str] = None
    #项目代码
    project_code:Optional[str] = None
    #采购人
    pur_org_name:Optional[str] = None
    #选取方式
    select_mode_type_name:Optional[str] = None
    #项目状态
    biz_status_name:Optional[str] = None
    #中选机构名称
    first_agent_name:Optional[str] = None
    #投资审批项目
    is_investment_project:Optional[bool] = None
    #项目规模
    #资金来源
    #项目实施地行政区划
    implement_division_code_name:Optional[str] = None
    #是否为行政管理中介服务事项采购
    is_approval_service_project:Optional[bool] = None
    #所需服务类型
    service_type_name:Optional[str] = None
    #服务金额
    service_price:Optional[str] = None
    #金额说明
    price_description:Optional[str] = None
    #选取时间
    select_time:Optional[datetime] = None
    #选取结束时间
    select_finish_time:Optional[date] = None
    #中选机构联系地址
    office_address:Optional[str] = None
    #中选金额
    price_str:Optional[str] = None
    #机构证件号
    first_agent_account:Optional[str] = None
    #链接
    link:Optional[str] = None
