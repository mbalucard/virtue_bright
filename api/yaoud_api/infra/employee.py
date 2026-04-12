"""
员工管理
    - 员工角色及系统可用角色列表-下拉检索用: employee_organ_post_list
    - 获取员工信息列表: employee_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/employee"

async def employee_organ_post_list(
        authorization: str,
        organId: int,
        employeeId: Optional[int] = None,
        tenant_id: Optional[int] = None,) -> dict:
    """
    员工角色及系统可用角色列表-下拉检索用
    Args:
        authorization (str): 认证信息
        organId (int): 机构ID
        employeeId (int, None): 员工ID. Defaults to None.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 
    """
    url = f"{base_url}/getEmpOrganPostList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "employeeId": employeeId,
        "organId": organId,  # 可在available_institutions_list中获取
        "systemType": 2,  # ? 用途未知
        "systemId": 1,  # ? 用途未知
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        yaoudAccount: Optional[str] = None,
        virtualYaoudAccount: Optional[str] = None,
        ids: Optional[List[str]] = None,
        status: Optional[int] = None,
        accountStatus: Optional[str] = None,
        sex: Optional[str] = None,
        birthDate: Optional[str] = None,
        idNo: Optional[str] = None,
        graduateSchool: Optional[str] = None,
        speciality: Optional[str] = None,
        positionTitle: Optional[str] = None,
        postCodeList: Optional[List[str]] = None,
        education: Optional[str] = None,
        entryTimeStart: Optional[str] = None,
        entryTimeEnd: Optional[str] = None,
        positionType: Optional[str] = None,
        enterpriseId: Optional[List[str]] = None,
        organFormStr: Optional[str] = None,) -> dict:
    """
    获取员工信息列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        keyword (str, None): 关键字.Defaults to None.
            - 可搜索员工姓名，手机号,助记码. 
        yaoudAccount (str, None): 药德账号. Defaults to None.
        virtualYaoudAccount (str, None): 虚拟药德账号. Defaults to None.
        ids (List[str], None): 员工ID列表. Defaults to None.
        status (int, None): 员工状态. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为员工状态.
        accountStatus (str, None): 账号状态. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为账号状态.
        sex (str, None): 性别. Defaults to None.
            - 1:男
            - 2:女
        birthDate (str, None): 出生日期. Defaults to None.
            - 日期格式为yyyy-MM-dd
        idNo (str, None): 证件号码. Defaults to None.
        graduateSchool (str, None): 毕业学校. Defaults to None.
        speciality (str, None): 专业. Defaults to None.
        positionTitle (str, None): 职称. Defaults to None.
        #! 该参数枚举值貌似拿掉了，现在改为字符串
            - master：主任医师
            - doctor：副主任医师
            - chief_nurse：主任护士
            - nurse：副主任护士
            - master_pharmacist：主任药师
            - pharmacist：副主任药师
            - master_technician：主任技师
            - technician：副主任技师
        postCodeList (List[str], None): 角色编码列表. Defaults to None. 
            - 可在 employee_organ_post_list 中获取
        education (str, None): 学历. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为学历.
        entryTimeStart (str, None): 入职开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd.
        entryTimeEnd (str, None): 入职结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd.
        positionType (str, None): 在职类型. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为在职类型.
        enterpriseId (List[str], None): 节点名称. Defaults to None.
            - 可在 get_block_enterprise_tree 中获取 对应字段 key
        organFormStr (str, None): 与enterpriseId联动使用. Defaults to None.
    Returns:
        dict: 员工列表
    """
    url = f"{base_url}/pagePost"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    order_fields = [{"field": "name", "order": None}, {"field": "nameAbc", "order": None}, {"field": "code", "order": None}, {"field": "telephone", "order": None}, {"field": "sex", "order": None}, {"field": "birthDate", "order": None}, {"field": "status", "order": None}, {"field": "idNo", "order": None}, {"field": "entryTime", "order": None}, {"field": "positionType", "order": None}, {
        "field": "speciality", "order": None}, {"field": "graduateSchool", "order": None}, {"field": "education", "order": None}, {"field": "positionTitle", "order": None}, {"field": "yaoudAccount", "order": None}, {"field": "enterpriseList", "order": None}, {"field": "virtualYaoudAccount", "order": None}, {"field": "leaveTime", "order": None}, {"field": "organNames", "order": None}, {"field": "accountStatus", "order": None}]
    if entryTimeStart:
        entry_time_start = get_date_start_and_end_time(entryTimeStart)
    else:
        entry_time_start = None
    if entryTimeEnd:
        entry_time_end = get_date_start_and_end_time(entryTimeEnd)
    else:
        entry_time_end = None
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "yaoudAccount": yaoudAccount,
        "virtualYaoudAccount": virtualYaoudAccount,
        "ids": ids,
        "status": status,
        "accountStatus": accountStatus,
        "sex": sex,
        "birthDate": birthDate,
        "idNo": idNo,
        "graduateSchool": graduateSchool,
        "speciality": speciality,
        "positionTitle": positionTitle,
        "postCodeList": postCodeList,  # ! 该参数已失效
        "education": education,
        "entryTimeStart": entry_time_start['start_time'] if entry_time_start else None,
        "entryTimeEnd": entry_time_end['end_time'] if entry_time_end else None,
        "positionType": positionType,
        "enterpriseId": enterpriseId,
        "organFormStr": organFormStr,
        "orderFields": order_fields,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_info(
        authorization: str,
        employee_id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    获取员工信息详情
    Args:
        authorization (str): 认证信息
        employee_id (int): 员工ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 员工信息详情
    """
    url = f"{base_url}/info"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": employee_id,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

