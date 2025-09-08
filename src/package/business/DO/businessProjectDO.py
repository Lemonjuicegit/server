from sqlmodel import SQLModel, Relationship
from package.database import TYPE
from datetime import date


class BusinessProjectDO(SQLModel, table=True):
    __tablename__ = "business_project"
    id: int = TYPE.PRIMARY_KEY
    company: str  # 公司名称
    code: str  # 项目编号
    name: str  # 项目名称
    region_code: str  # 项目区域
    source: str  # 项目来源
    contacts: str  # 联系人
    telephone: str  # 联系电话
    cooperation_type: str  # 合作/完成方式，自有、合作、挂靠
    dept_id: int  # 责任部门
    user_id: int  # 负责人ID
    notes: str  # 备注
    archiving_status: str  # 成果归档状态，归档，未归档
    archiving_user_id: int  # 成果归档人员
    archiving_date: date  # 成果归档日期
    creator: str  # 创建人
    create_time: date  # 创建时间
    update_time: date  # 更新时间
    updater: str  # 更新人
    deleted: int  # 是否删除
    status: int  # 项目状态
    process_instance_id: str  #
    result: str  #
    classification: int  # 项目分类
    content: str  # 工作内容
    introducer: str  # 介绍人
    introducer_tel: str  # 介绍人电话
    amounts: float  # 实际总金额
    talks_user: str  # 项目谈判人员
    follow_user_id: int  # 跟踪人员（选择）
    performance_bond: float  # 履约保证金
    performance_bond_status: int  # 履约保证金收回状态（选择）
    info_source: str  # 信息来源
    dept_nature: str  # 单位性质
    need_contract: int  # 是否需要合同
    achieve_status: int  # 归档状态
    achiever: int  # 归档人
    achiever_name: str  # 归档人
    achieve_date: date  # 归档时间
    opportunity_id: int  #
    estimated_amount: float  # 预估总金额
    estimated_cost: float  # 预估成本
    estimated_profit: float  # 预估利润
    planned_time: date  # 计划完成时间
    received_status: int  #
    contract_id: int  #
    information_providers: int  # 公司内部消息提供者
    head_marketing_id: int  # 市场负责人
    approval_time: date  # 立项时间
    current_progress_node: int  # 当前进度节点
    manage_overall_progress: int  # 项目总进度
    stocks_additions: int  # 存量与新增
    contract_status: int  # 合同状态
    payment: float  # 已收款(万元)
    unpaid: float  # 未收款(万元)
    invoiced: float  # 已开票(万元)
    not_invoiced: float  # 未开票(万元)
    invoiced_unpaid: float  # 已开票未回款(万元)
    not_invoiced_unpaid: float  # 未开票未收款(万元)
    registration_time: date  # 首次登记时间
    project_owner: str  # 业主单位
