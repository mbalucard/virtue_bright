"""
考勤管理
    - 考勤项-列表: checking_item_page
    - 考勤项-详情: checking_item_detail
    - 考勤项列表: checking_detail_items
    - 考勤表模版-列表: checking_template_page
    - 获取考勤模版: get_template_in_checking_table
    - 考勤搜索条件字段配置: checking_search_condition_fields
    - 考勤表头: checking_table_head
    - 考勤数据管理-考勤表: get_checking_data
    - 考勤数据管理-考勤提交任务: page_checking_task
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrChecking"
TTL = yaoud_env["timeout"]


async def checking_item_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        enabled: Optional[int] = None,
        dataType: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    考勤项-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        enabled (int, None): 是否启用. Defaults to None.
            - 1:启用 0:未启用
        dataType (int, None): 数据类型. Defaults to None.
            - 0:明细 1:汇总
        keyword (str, None): 关键字. Defaults to None.
            - 名称或编码
    Returns:
        dict: 考勤项-列表
    """
    url = f"{base_url}/pageCheckingItem"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "enabled": enabled,
        "dataType": dataType,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def checking_item_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    考勤项-详情
    Args:
        authorization (str): 认证信息
        id (int): 考勤项ID.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 考勤项-详情
    """
    url = f"{base_url}/detailCheckingItem/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def checking_detail_items(
        authorization: str,
        tenant_id: Optional[int] = None,
        checkingMonth: Optional[str] = None,
        templateId: Optional[int] = None,) -> dict:
    """
    考勤项列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        checkingMonth (str, None): 考勤月份. Defaults to None.
            - 格式:yyyyMM
        templateId (int, None): 考勤表模版ID. Defaults to None.
            - 可在 get_template_in_checking_table 中获取
    Returns:
        dict: 考勤项列表
    """
    url = f"{base_url}/checkingDetailItems"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not checkingMonth:
        checkingMonth = get_current_date().replace("-", "")
        checkingMonth = checkingMonth[:6]
    params = {
        "checkingMonth": checkingMonth,
        "templateId": templateId,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def checking_template_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        keyword: Optional[str] = None,) -> dict:
    """
    考勤表模版-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - 名称或编码
    Returns:
        dict: 考勤表模版-列表
    """
    url = f"{base_url}/pageCheckingTemplate"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def get_template_in_checking_table(
        authorization: str,
        tenant_id: Optional[int] = None,
        checkingMonth: Optional[str] = None,) -> dict:
    """
    获取考勤模版
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        checkingMonth (str, None): 考勤月份. Defaults to None.
            - 格式:yyyyMM
    Returns:
        dict: 获取考勤模版
    """
    url = f"{base_url}/getTemplateInCheckingTable"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not checkingMonth:
        checkingMonth = get_current_date().replace("-", "")
        checkingMonth = checkingMonth[:6]
    payload = {
        "checkingMonth": checkingMonth
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def checking_search_condition_fields(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    考勤搜索条件字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 考勤搜索条件字段配置
    """
    url = f"{base_url}/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def checking_table_head(
        authorization: str,
        tenant_id: Optional[int] = None,
        checkingMonth: Optional[str] = None,
        templateId: Optional[int] = None,) -> dict:
    """
    考勤表头
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        checkingMonth (str, None): 考勤月份. Defaults to None.
            - 格式:yyyyMM
        templateId (int, None): 考勤表模版ID. Defaults to None.
            - 可在 get_template_in_checking_table 中获取
    Returns:
        dict: 考勤表头
    """
    url = f"{base_url}/checkingTableHead"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not checkingMonth:
        checkingMonth = get_current_date().replace("-", "")
        checkingMonth = checkingMonth[:6]
    params = {
        "checkingMonth": checkingMonth,
        "templateId": templateId,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def get_checking_data(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        checkingMonth: Optional[str] = None,
        checkingPowerManage: int = 0,
        templateId: Optional[int] = None,
        name: Optional[str] = None,
        workNo: Optional[str] = None,
        employeeStatus: Optional[List[str]] = None,
        positiveStatus: Optional[List[str]] = None,
        checkingOrgList: Optional[List[str]] = None,
        organization: Optional[List[str]] = None,
        position: Optional[List[str]] = None,
        actualPositiveDate: Optional[List[str]] = None,
        entryDate: Optional[List[str]] = None,
        leaveDate: Optional[List[str]] = None,
        planPositiveDate: Optional[List[str]] = None,
        trialPeriodStartDate: Optional[List[str]] = None,
        ) -> dict:
    """
    考勤数据管理-考勤表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        checkingMonth (str, None): 考勤月份. Defaults to None.
            - 格式:yyyyMM
        checkingPowerManage (int): 考勤权限管理. Defaults to 0.
            - 0:否 1:是
        templateId (int, None): 考勤表模版ID. Defaults to None.
            - 可在 get_template_in_checking_table 中获取
        name (str, None): 姓名. Defaults to None.
        workNo (str, None): 工号. Defaults to None.
        employeeStatus (List[str], None): 员工状态. Defaults to None.
            - onJob:在职, leaveJob:离职
        positiveStatus (List[str], None): 转正状态. Defaults to None.
            - NoTrial:无试用期, Trial:试用期, Regular:转正
        checkingOrgList (List[str], None): 考勤组织列表. Defaults to None.
            - 可在 department_tree 中获取 对应字段 mainTableId
        organization (List[str], None): 组织. Defaults to None.
            - 可在 department_tree 中获取 对应字段 mainTableId
        position (List[str], None): 职位. Defaults to None.
            - 可在 position_list 中获取 对应字段 mainTableId
        actualPositiveDate (List[str], None): 实际转正日期区间. Defaults to None.
            - 格式:yyyy-MM-dd
            - 样例:["2026-01-01", "2026-01-02"]
        entryDate (List[str], None): 入职日期区间. Defaults to None.
            - 格式:yyyy-MM-dd
            - 样例:["2026-01-01", "2026-01-02"]
        leaveDate (List[str], None): 离职日期区间. Defaults to None.
            - 格式:yyyy-MM-dd
            - 样例:["2026-01-01", "2026-01-02"]
        planPositiveDate (List[str], None): 计划转正日期区间. Defaults to None.
            - 格式:yyyy-MM-dd
            - 样例:["2026-01-01", "2026-01-02"]
        trialPeriodStartDate (List[str], None): 试用期日期区间. Defaults to None.
            - 格式:yyyy-MM-dd
            - 样例:["2026-01-01", "2026-01-02"]
    Returns:
        dict: 考勤数据管理-考勤表
    """
    url = f"{base_url}/getCheckingData"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not checkingMonth:
        checkingMonth = get_current_date().replace("-", "")
        checkingMonth = checkingMonth[:6]
    payload = {
        "current": current,
        "size": size,
        "checkingMonth": checkingMonth,
        "checkingPowerManage": checkingPowerManage,
        "templateId": templateId,
        "name": name,
        "workNo": workNo,
        "employeeStatus": employeeStatus,
        "positiveStatus": positiveStatus,
        "checkingOrgList": checkingOrgList,
        "organization": organization,
        "position": position,
        "actualPositiveDate": actualPositiveDate,
        "entryDate": entryDate,
        "leaveDate": leaveDate,
        "planPositiveDate": planPositiveDate,
        "trialPeriodStartDate": trialPeriodStartDate,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()

async def page_checking_task(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        checkingMonth: Optional[str] = None,
        pushDateStart: Optional[str] = None,
        pushDateEnd: Optional[str] = None,) -> dict:
    """
    考勤数据管理-考勤提交任务
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        checkingMonth (str, None): 考勤月份. Defaults to None.
            - 格式:yyyyMM
        pushDateStart (str, None): 推送日期区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        pushDateEnd (str, None): 推送日期区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 考勤数据管理-考勤提交任务
    """
    url = f"{base_url}/pageCheckingTask"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not checkingMonth:
        checkingMonth = get_current_date().replace("-", "")
        checkingMonth = checkingMonth[:6]
    payload = {
        "current": current,
        "size": size,
        "checkingMonth": checkingMonth,
        "pushDateStart": pushDateStart,
        "pushDateEnd": pushDateEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()




if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_e989f1a7-81ea-453e-b282-f0e79a3494af"
    tenant_id = 148

    async def main():
        data = await page_checking_task(
            authorization=authorization,
            tenant_id=tenant_id,
            checkingMonth="202603",
        )
        print(data)
    asyncio.run(main())
