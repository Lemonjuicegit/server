from sqlmodel import SQLModel,JSON,Field
from src.package.database import TYPE
from typing import Optional,Dict  
from datetime import datetime
import uuid


class CgggDO(SQLModel, table=True):
    __tablename__ = "cggg"
    id: uuid.UUID = TYPE.PRIMARY_KEY
    #项目名称
    project_name: Optional[str] = None
    #采购人
    pur_org_name:Optional[str] = None
    #选取方式
    select_mode_type_name:Optional[str] = None
    #项目状态
    status_project:Optional[str] = None
    #公告时间
    time_announcement:Optional[datetime] = None
    #资质（资格）要求
    qual:Optional[list[Dict]] = Field(sa_type=JSON)
    #投资审批项目
    is_investment_project:Optional[bool] = None
    #是否为行政管理中介服务事项采购
    is_approval_service_project:Optional[bool] = None
    #项目代码
    project_code:Optional[str] = None
    #项目类型
    project_type:Optional[str] = None
    #选取时间
    select_time:Optional[datetime] = None
    #选取地址
    select_address:Optional[str] = None
    #创建者帐户
    creator_account:Optional[str] = None
    #创建者单位帐户
    creator_unit_account:Optional[str] = None
    #服务内容
    servcie_content:Optional[str] = None
    #资质（资格）要求说明
    qual_require:Optional[str] = None
    #服务时限及说明
    service_time_limit:Optional[str] = None
    #其他要求说明
    other_requirements:Optional[str] = None
    #所需服务类型
    service_type_name:Optional[str] = None
    #合同签订时限及说明
    contract_sign_time_limit:Optional[str] = None
    #服务金额
    service_price:Optional[str] = None
    #金额说明
    price_description:Optional[str] = None
    #项目实施地行政区划
    division_code_name:Optional[str] = None
    #链接
    link:Optional[str] = None
