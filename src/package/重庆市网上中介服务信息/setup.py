from .web_scraper import WebScraper
import requests
import uuid
import json
import time
from bs4 import BeautifulSoup,Tag, NavigableString
from datetime import datetime
from src.package.重庆市网上中介服务信息.database import cggg_service,jggg_service,zjjg_service
def get_soup():
    zj_url = r'https://zjcs.cqggzy.com/cq-zjcs-pub/zjfw/agentList'
    cg_url = r'https://zjcs.cqggzy.com/cq-zjcs-pub/purchaseNotice'
    jg_url = r'https://zjcs.cqggzy.com/cq-zjcs-pub/bidResultNotice'
    zj_scr = WebScraper(zj_url)
    cg_scr = WebScraper(cg_url)
    jg_scr = WebScraper(jg_url)
    return zj_scr, cg_scr, jg_scr
def rem_none(data):
    return [v for v in data if v is not None]

def get_headers(cookie=None):
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
    }
    if isinstance(cookie, requests.cookies.RequestsCookieJar):
        for key, value in cookie.get_dict().items():
            cookiestr += key + '=' + value + ';'
        default_headers['Cookie'] = cookie
    return default_headers

def set_cookies(cookies):
    cookiestr = ''
    for key, value in cookies.get_dict().items():
        cookiestr += key + '=' + value + ';'
    return cookiestr

def element_to_tree(element):
    """
    将BeautifulSoup元素转换为树形结构字典，每个节点只保留第一个直接子元素的文本
    """
    # 如果是文本节点，返回文本
    if isinstance(element, NavigableString):
        text = str(element).strip()
        return {"text": text} if text else None
    
    # 如果不是标签元素，返回None
    if not isinstance(element, Tag):
        return None
    
    # 初始化当前节点的字典
    node = {
        "tag": element.name,
        "text": None,  # 先置空，后面找第一个直接文本子节点
        "children": []
    }
    
    # 查找第一个直接文本子节点
    for child in element.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:  # 只保留非空白文本
                node["text"] = text
                break  # 找到第一个就停止
    
    # 递归处理所有子标签元素
    for child in element.children:
        if isinstance(child, Tag):  # 只处理标签子元素
            child_node = element_to_tree(child)
            if child_node:
                node["children"].append(child_node)
    return node
def filter_li_nodes(node):
    """
    递归过滤树形结构，只保留li标签的节点，保持嵌套关系
    """
    # 非字典类型直接返回None（处理边界情况）
    if not isinstance(node, dict):
        return None
    
    # 递归处理所有子节点，过滤出其中的li节点
    filtered_children = []
    if "children" in node:
        for child in node["children"]:
            processed_child = filter_li_nodes(child)
            if processed_child:
                # 如果子节点处理后是列表（多个li节点），则展开添加
                if isinstance(processed_child, list):
                    filtered_children.extend(processed_child)
                else:
                    filtered_children.append(processed_child)
    
    # 如果当前节点是li标签，保留该节点并更新子节点为过滤后的结果
    if node.get("tag") in ["li","a"] and node.get("text") is not None:
        if filtered_children:
            return {
                "text": node.get("text"),  # 保留原text（包括null）
                "children": filtered_children
            }
        else:
            return {
                "text": node.get("text"),  # 保留原text（包括null）
            }
    # 如果不是li标签，但有过滤后的子节点，返回这些子节点（确保嵌套关系不中断）
    elif filtered_children:
        return filtered_children
    # 既不是li标签也没有有效子节点，返回None
    else:
        return None
def get_table_data(soup,url_callback=None):
    # zj_html = scr.form_html(form_data,url)
    # soup = BeautifulSoup(scr, 'html.parser')
    table_element = soup.select('table.table-bordered')[0]
    # return zj_html 
    # 提取表头
    headers = []
    header_row = table_element.find('tr')
    if header_row:
        header_cells = header_row.find_all(['th', 'td'])
        headers = [cell.get_text(strip=True) for cell in header_cells]
    # 提取数据行
    rows = []
    for row in table_element.find_all('tr')[1:]:  # 跳过表头行
        cells = row.find_all(['td', 'th'])
        a_elem = row.find('a')
        if not a_elem:
            continue
        href = a_elem.get('href')
        if url_callback:
            project_code = url_callback(href)
        else:
            project_code = href
        if cells:  # 确保行中有单元格
            row_data = [cell.get_text(strip=True).replace(',','，').replace('\n','') for cell in cells]
            # 确保每行数据与表头数量一致
            if len(row_data) < len(headers):
                # 如果数据列少于表头列，用空字符串填充
                row_data.extend([''] * (len(headers) - len(row_data)))
            elif len(row_data) > len(headers):
                # 如果数据列多于表头列，截断多余的数据
                row_data = row_data[:len(headers)]
            
            row_data.append(project_code)
            rows.append(row_data)
    return rows

def set_cg_item(row,table_data):
    item = {'project_name':row['projectName'],
        'pur_org_name':row['purOrgName'],
        'select_mode_type_name':table_data[3],
        'status_project':table_data[4],
        'time_announcement':datetime.strptime(table_data[5],"%Y-%m-%d %H:%M:%S"),
        'id':row['id'],
        'is_investment_project':row['isInvestmentProject'],
        'project_code':row['projectCode'],
        'project_type':row['projectType'],
        'publish_date':datetime.strptime(row['publishDate'],"%Y-%m-%d").date(),
        'select_time':datetime.strptime(row['selectTime'],"%Y-%m-%d %H:%M:%S"),
        'select_address':row['selectAddress'],
        'creator_account':row['creatorAccount'],
        'creator_unit_account':row['creatorUnitAccount'],
        'restrictions_forehead_type':row['restrictionsForeheadType'],
        'restrictions_forehead':row['restrictionsForehead'],
        'restrictions_forehead_str':row['restrictionsForeheadStr'],
        'servcie_content':row['servcieContent'],
        'qual_require':row['qualRequire'],
        'qual':row['qual'],
        'service_time_limit':row['serviceTimeLimit'],
        'other_requirements':row['otherRequirements'],
        'service_type_name':row['serviceTypeName'],
        'contract_sign_time_limit':row['contractSignTimeLimit'],
        'service_price':row['servicePrice'],
        'price_description':row['priceDescription'],
        'link':f"https://zjcs.cqggzy.com/cq-zjcs-pub/purchaseNotice/view/{row['projectCode']}",
        'publish_datestr':row['publishDateStr'],
        'select_time_str':row['selectTimeStr'],
        'restrictions_frehead_type':row['restrictionsForeheadType'],
        'select_type':row['selectType'],
        'qual_item_relation':row['qualItemRelation'],
        'total_service_price':row['totalServicePrice'],
        'low_price':row['lowPrice'],
        'high_price':row['highPrice'],
        'bidding_mode':row['biddingMode'],
        'is_confirm_price':row['isConfirmPrice'],
        'confirm_price_type':row['confirmPriceType'],
        'is_public':row['isPublic'],
        'show_agent_after_finish':row['showAgentAfterFinish'],
        'biz_status':row['bizStatus'],
        'select_count':row['selectCount'],
        'is_reward_agent':row['isRewardAgent'],
        'is_show_reward_agent':row['isShowRewardAgent'],
        'sign_up_end_time':datetime.strptime(row['signUpEndTime'],"%Y-%m-%d %H:%M:%S"),
        'sign_up_end_time_str':row['signUpEndTimeStr'],
        'sign_up_end_time_mm_str':row['signUpEndTimeMmStr'],
        'consult_phone':row['consultPhone'],
        'complaints_hotline':row['complaintsHotline'],
        'is_revision':row['isRevision'],
        'select_type_name':row['serviceTypeName'],
        'division_code_name':row['divisionCodeName'],
        'attachment_vo_list':row['attachmentVoList'],
        'is_registerd':row['isRegisterd'],
        'data_content':row['dataContent'],
        'rest_str':row['restStr'],
        'sign_up_count':row['signUpCount'],
        'approval_org_name':row['approvalOrgName'],
        'select_agent_name':row['selectAgentName'],
        'note':row['note'],
        'is_avoided':row['isAvoided'],
        'avoided_agents_name':row['avoidedAgentsName'],
        'avoided_reason':row['avoidedReason'],
        'admin_status':row['adminStatus'],
        'select_mode_type':row['selectModeType'],
        'inquiry_round':row['inquiryRound'],
        'perhaps_bidding_mode':row['perhapsBiddingMode'],
        'perhaps_price':row['perhapsPrice'],
        'sfdchy':row['sfdchy'],
        'biz_division_code':row['bizDivisionCode'],
        'is_approval_service_project':row['isApprovalServiceProject'],
        'implement_division_code_name':row['implementDivisionCodeName'],
        'approval_dep_division_code_name':row['approvalDepDivisionCodeName'],
        'biz_division_code_name':row['bizDivisionCodeName'],
        'service_subject_name':row['serviceSubjectName'],
        'agent_subject_vo_id':row['agentSubjectVoId'],
        'fund_source':row['fundSource'],
        'is_investment_project':row['isInvestmentProject'],
        'vc_process_project_code':row['vcProcessProjectCode'],
        'qual_level_item_name':row['qualLevelItemName'],
        'pur_dept_archives_evaluation_source':row['purDeptArchivesEvaluationSource'],
        'zjfwjgyq':row['zjfwjgyq'],
        'practitioners_count':row['practitionersCount'],
        'practitioners_require':row['practitionersRequire'],
        'bayqsm':row['bayqsm'],
        'service_type_claim':row['serviceTypeClaim'],
        'bs_revision_reason':row['bsRevisionReason'],
        'bs_revision_last_modified_date':row['bsRevisionLastModifiedDate'],
        'bs_revision_last_modified_date_str':row['bsRevisionLastModifiedDateStr'],
        'parent_project_name':row['parentProjectName'],
        'selection_subject':row['selectionSubject'],
        'case_no':row['caseNo'],
        'debtor_situation':row['debtorSituation'],
        'is_pcft_project':row['isPcftProject'],
        'is_pcft_creator':row['isPcftCreator'],
        'life_cycle_status':row['lifeCycleStatus'],
        'life_publish_date':row['lifePublishDate'],
        'life_publish_date_str':row['lifePublishDateStr'],
        'bid_result_time':row['bidResultTime'],
        'bid_result_time_str':row['bidResultTimeStr'],
        'contract_time':row['contractTime'],
        'contract_time_str':row['contractTimeStr'],
        'service_finish_time':row['serviceFinishTime'],
        'service_finish_time_str':row['serviceFinishTimeStr'],
        'push_gcjsxt':row['pushGcjsxt'],
    }
    for k,v in item.items():
        if isinstance(v,str):
            item[k] = v.replace('\n','').replace('\r','').replace('\t','').replace(',','，')
    return item

def set_jg_item(row,table_data):
    item = {
        'id':uuid.uuid4(),
        'project_name':row['projectName'],
        'project_code':row['projectCode'],
        'pur_org_name':row['purOrgName'],
        'select_mode_type_name':row['selectModeTypeName'],
        'biz_status_name':table_data[4],
        'first_agent_name':row['firstAgentName'],
        'is_investment_project':row['isInvestmentProject'],
        'implement_division_code_name':row['implementDivisionCodeName'],
        'is_approval_service_project':row['isApprovalServiceProject'],
        'service_type_name':row['serviceTypeName'],
        'service_price':row['servicePrice'],
        'price_description':row['priceDescription'],
        'select_time':datetime.strptime(row['selectTime'],"%Y-%m-%d %H:%M:%S"),
        'select_finish_time':datetime.strptime(table_data[6],"%Y-%m-%d").date(),
        'office_address':row['officeAddress'],
        'price_str':row['priceStr'],
        'first_agent_account':row['firstAgentAccount'],
        'link':f"https://zjcs.cqggzy.com/cq-zjcs-pub/bidResultNotice/view/{row['projectCode']}"
    }
    for k,v in item.items():
        if isinstance(v,str):
            item[k] = v.replace('\n','').replace('\r','').replace('\t','').replace(',','，')
    return item

def set_soup(headers,request_type='get'):
    def get_soup(url,data=None):
        if request_type == 'get':
            res = requests.get(url,headers=headers)
        elif request_type == 'post':
            res = requests.post(url,data=data,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        return soup
    return get_soup

def get_zz(id,headers):
    #获取资质
    zz_zpi = f"https://zjcs.cqggzy.com/cq-zjcs-pub/purchaseNotice/qualityMultiView/{id}"
    res = requests.get(zz_zpi,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    treeDiv = soup.find('div',class_='serviceType')

    return treeDiv

def get_bidResultNotice(headers,project_code):
    api_str = fr'https://zjcs.cqggzy.com/cq-zjcs-pub/api/bidResultNotice/view/{project_code}'
    res = requests.get(api_str,headers=headers)
    return res

def get_purchaseNotice(headers,project_code):
    api_str = fr'https://zjcs.cqggzy.com/cq-zjcs-pub/api/purchaseNotice/view/{project_code}'
    res = requests.get(api_str,headers=headers)
    return res

def get_archivesContact(row):
    default_headers = {
        'cookie':'JSESSIONID=C9AE34E1C56ED7128B15585967B08911; __jsluid_s=47795fd533af3078b87772179e2a88db; Cookie-92=25223204; Hm_lvt_ea823d3b05c47602cfcccc405d8a349f=1756461131,1756626199; Hm_lpvt_ea823d3b05c47602cfcccc405d8a349f=1756626199; HMACCOUNT=B64F5A253130C57C; __jsl_clearance_s=1756788870.049|0|vhjovtJ59fYTlZ9HSh15T%2FswOOw%3D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
    }
    html = requests.get(row.link,headers=default_headers)
    soup = BeautifulSoup(html.text,features="lxml")
    table = soup.select('table.pannel-cont-table')[1]
    tr = table.select('tr')
    row_list = list(row)
    for i in tr:
        row_list.append(i.select('td')[1].text)
    
    return row_list

def insert_cggg(count = 1000):
    listPost_api = r'https://zjcs.cqggzy.com/cq-zjcs-pub/purchaseNotice/listPost'
    cg_url = r'https://zjcs.cqggzy.com/cq-zjcs-pub/purchaseNotice'
    headers = get_headers()
    cg_scr = requests.get(cg_url,headers=headers)
    headers['Cookie'] = set_cookies(cg_scr.cookies)
    get_soup = set_soup(headers,'post')
    url_callback = lambda x: x.split('/')[-1]
    n = 0
    exist_limit = 5
    exist_count = 0
    for i in range(count):
        if exist_count >= exist_limit:
            break
        cg_form_data = {
            'listVo.projectName': '',
            'listVo.divisionCode':'500000',
            'listVo.purOrgName':'',
            'listVo.publishDateBegin':'',
            'listVo.publishDateEnd':'',
            'listVo.selectType':'',
            'serviceType_selectname':'',
            'selectBox_serviceType':'',
            'listVo.serviceType':'',
            'listVo.serviceSubjectCode':'',
            'pageNumber':str(i),
            'sourtType':'',
        }
        soup =get_soup(listPost_api,cg_form_data)
        cg_scr_res = get_table_data(soup,url_callback)
        insert_list = []
        for row in cg_scr_res:
            select_data = cggg_service.select({'project_code':row[-1]})
            if select_data:
                if exist_count <= exist_limit:
                    exist_count+=1
                    continue
                else:
                    break
            
            # 添加重试机制获取采购公告
            retry_count = 3
            purchase = None
            for attempt in range(retry_count):
                try:
                    purchase = get_purchaseNotice(headers,row[-1]).json()
                    break
                except Exception as e:
                    if attempt < retry_count - 1:
                        time.sleep(0.5 * (2 ** attempt))  # 指数退避
                        continue
                    else:
                        raise e
            purchase_data = purchase['data']['purchaseNoticeViewVo']
            treeDiv = get_zz(purchase_data['id'],headers)
            qual_elem = element_to_tree(treeDiv)
            qual_res = filter_li_nodes(qual_elem)
            purchase_data['qual']=qual_res
            item = set_cg_item(purchase['data']['purchaseNoticeViewVo'],row)
            insert_list.append(item)

        n+=1
        if insert_list:  # 只有当有数据需要插入时才执行插入操作
            try:
                cggg_service.insert(insert_list)
            except Exception as e:
                print(f"插入数据时出错: {e}")
        time.sleep(0.5)
        print(f"{n}/{count}页:cggg",end="\r")

def insert_jggg(count = 1000):
    listPost_api = r'https://zjcs.cqggzy.com/cq-zjcs-pub/bidResultNotice/rest'
    jg_url = r'https://zjcs.cqggzy.com/cq-zjcs-pub/purchaseNotice'
    headers = get_headers()
    jg_scr = requests.get(jg_url,headers=headers)
    headers['Cookie'] = set_cookies(jg_scr.cookies)
    get_soup = set_soup(headers,'post')
    url_callback = lambda x: x.split('/')[-1]
    n = 0
    exist_limit = 5
    exist_count = 0
    for i in range(count):
        if exist_count >= exist_limit:
            break
        jg_form_data = {
            'listVo.projectName': '',
            'listVo.divisionCode': '500000',
            'listVo.purOrgName': '',
            'listVo.bidResultDateBegin': '',
            'listVo.bidResultDateEnd': '',
            'listVo.selectType': '',
            'serviceType_selectname': '',
            'selectBox_serviceType': '',
            'listVo.serviceType': '',
            'pageNumber': str(i),
            'sourtType': '',
        }
        soup =get_soup(listPost_api,jg_form_data)
        jg_scr_res = get_table_data(soup,url_callback)
        insert_list = []
        for row in jg_scr_res:
            select_data = jggg_service.select({'project_code':row[-1]})

            if select_data:
                if exist_count <= exist_limit:
                    exist_count+=1
                    continue
                else:
                    break
            purchase = get_bidResultNotice(headers,row[-1]).json()
            bidResult = purchase['data']['bidResultNoticeVo']
            bidResult.update( purchase['data']['bsBidResultVo'])
            item = set_jg_item(bidResult,row)
            insert_list.append(item)
        n+=1
        if insert_list:
            try:
                jggg_service.insert(insert_list)
            except Exception as e:
                print(f"插入数据时出错: {e}")
        time.sleep(0.5)
        print(f"{n}/{count}页:jggg",end="\r")