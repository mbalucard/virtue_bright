"""
人员管理
    - 人员列表: employee_list
    - 人员列表字段配置: employee_list_settings_fields
    - 人员花名册字段配置: employee_roster_field_setting
    - 人员搜索条件字段配置: employee_search_condition_fields
    - 人员名册: employee_page_list
    - 人员工作信息: employee_detail_work_info
    - 人事事件记录: hr_employee_tranct_log
    - 花名册详情: employee_detail_personal_info
    - 人事同步日志-人员: employee_sync_log
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrEmployee"


async def employee_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        basicDate: str = get_current_date(),) -> dict:
    """
    人员列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        basicDate (str): 基础日期. Defaults today .
            - 格式:yyyy-MM-dd
    Returns:
        dict: 人员列表
    """
    url = f"{base_url}/employee/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "basicDate": basicDate,
        "_": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_list_settings_fields(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    人员列表字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员列表字段配置
    """
    url = f"{base_url}/listSettingsFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_roster_field_setting(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    人员花名册字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员花名册字段配置
    """
    url = f"{base_url}/rosterFieldSetting"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_search_condition_fields(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    人员搜索条件字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员搜索条件字段配置
    """
    url = f"{base_url}/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_page_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        conditions: Optional[List[dict]] = None,) -> dict:
    """
    人员名册
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        conditions (List[dict], None): 检索条件. Defaults to None.
            - 可在 employee_search_condition_fields 中获取人员检索信息
            - 可在 position_list 中获取职位检索信息
            - 样例: [{"field":"basicDate","title":"基准日期","rule":"eq","ruleName":"等于","value":"2026-03-31","labelValue":"","valueType":8}]
    Returns:
        dict: 人员名册
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "conditions": conditions,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_detail_work_info(
        authorization: str,
        id: int,
        version_id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    人员工作信息
    Args:
        authorization (str): 认证信息
        id (int): 人员ID.
            - 可在 employee_page_list 中获取  对应字段 id
        version_id (int): 版本ID.
            - 可在 employee_page_list 中获取  对应字段 versionId
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员工作信息
    """
    url = f"{base_url}/detail/workInfo/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "versionId": version_id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def hr_employee_tranct_log(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    employeeName: Optional[str] = None,
    workPlaceName: Optional[str] = None,
    eventTypeName: Optional[str] = None,
    versionStatus: Optional[int] = None,
    jobType: Optional[List[str]] = None,
    positiveStatus: Optional[str] = None,
    organization: Optional[List[str]] = None,
    positionClassification: Optional[str] = None,
    directLeader: Optional[str] = None,
    businessAgent: Optional[str] = None,
    startTime: Optional[str] = None,
    endTime: Optional[str] = None,
    effectiveDate: Optional[str] = None,
    expirationDate: Optional[str] = None,
    entryDate: Optional[str] = None,
    trialPeriodStartDate: Optional[str] = None,
    planPositiveDate: Optional[str] = None,
    actualPositiveDate: Optional[str] = None,
    leaveDate: Optional[str] = None,) -> dict:
    """
    人事事件记录
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        employeeName (str, None): 员工姓名. Defaults to None.
        workPlaceName (str, None): 工作地点. Defaults to None.
        eventTypeName (str, None): 事件类型. Defaults to None.
            #! 这里居然用的是汉字，佩服
            - 审批中 被驳回 已撤回 待生效 已生效
        versionStatus (int, None): 事件状态. Defaults to None.
            - 1:入职 2:转正 3:异动 4:离职 5:原工号重新雇佣 6:新工号重新雇佣
        jobType (List[str], None): 在职类型. Defaults to None.
            - 1:全职 2:兼职 3:外聘 4:后勤
        positiveStatus (str, None): 转正状态. Defaults to None.
            - 可在 employee_search_condition_fields 中获取 对应field=positiveStatus
        organization (List[str], None): 组织架构. Defaults to None.
            - 可在 department_tree 中获取 对应字段id
        positionClassification (str, None): 职位分类. Defaults to None.
            - 可在 position_classification_list 中获取 对应字段id
        directLeader (str, None): 直属上级. Defaults to None.
            - 可在 employee_list 中获取 对应字段id
        businessAgent (str, None): 业务代理人. Defaults to None.
            - 可在 employee_list 中获取 对应字段id
        startTime (str, None): 创建日期区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        endTime (str, None): 创建日期区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        effectiveDate (str, None): 生效日期. Defaults to None.
            - 格式:yyyy-MM-dd
        expirationDate (str, None): 失效日期. Defaults to None.
            - 格式:yyyy-MM-dd
        entryDate (str, None): 入职日期. Defaults to None.
            - 格式:yyyy-MM-dd
        trialPeriodStartDate (str, None): 试用期开始日期. Defaults to None.
            - 格式:yyyy-MM-dd
        planPositiveDate (str, None): 转正日期. Defaults to None.
            - 格式:yyyy-MM-dd
        actualPositiveDate (str, None): 实际转正日期. Defaults to None.
            - 格式:yyyy-MM-dd
        leaveDate (str, None): 离职日期. Defaults to None.
            - 格式:yyyy-MM-dd
        #! 缺少职级参数，因无数据，无法测试
    Returns:
        dict: 人事事件记录
    """
    url = f"{base_url}WorkInfoVersion/hrEmployeeTranctLog"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "employeeName": employeeName,
        "workPlaceName": workPlaceName,
        "eventTypeName": eventTypeName,
        "versionStatus": versionStatus,
        "jobType": jobType,
        "positiveStatus": positiveStatus,
        "organization": organization,
        "positionClassification": positionClassification,
        "directLeader": directLeader,
        "businessAgent": businessAgent,
        "startTime": startTime if startTime else get_current_date(),
        "endTime": endTime if endTime else get_current_date(),
        "effectiveDate": effectiveDate,
        "expirationDate": expirationDate,
        "entryDate": entryDate,
        "trialPeriodStartDate": trialPeriodStartDate,
        "planPositiveDate": planPositiveDate,
        "actualPositiveDate": actualPositiveDate,
        "leaveDate": leaveDate,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def employee_detail_personal_info(
    authorization: str,
    employeeId: int,
    versionId: Optional[int] = None,
    tenant_id: Optional[int] = None,) -> dict:
    """
    花名册详情
    Args:
        authorization (str): 认证信息
        employeeId (int): 人员ID.
            - 可在 employee_page_list 中获取  对应字段 id
        versionId (int, None): 版本ID. Defaults to None.
            - 可在 employee_page_list 中获取  对应字段 versionId
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 花名册详情
    """
    url = f"{base_url}/detail/personalInfo/{employeeId}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "versionId": versionId,  #! 这个参数给不给都能获取到数据
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()



async def employee_sync_log(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    syncType: Optional[str] = None,
    syncMethod: Optional[int] = None,
    syncSystem: Optional[int] = None,
    syncTimeStart: Optional[str] = None,
    syncTimeEnd: Optional[str] = None,)->dict:
    """
    人事同步日志-人员
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - 支持姓名 工号
        status (str, None): 状态. Defaults to None.
            - 0:失败 1:成功
        syncType (str, None): 同步类型. Defaults to None.
            - 1:新增 2:变更 3:删除
        syncMethod (int, None): 同步类别. Defaults to None.
            - 0:回传 1:推送
        syncSystem (int, None): 同步系统. Defaults to None.
            - 1:药德 2:企业微信 3:飞书
        syncTimeStart (str, None): 同步时间开始. Defaults to None.
            - 格式:yyyy-MM-dd
        syncTimeEnd (str, None): 同步时间结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 人事同步日志-人员
    """
    url = f"{base_url}/querySyncLog"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "status": status,
        "syncType": syncType,
        "syncMethod": syncMethod,
        "syncSystem": syncSystem,
        "syncTimeStart": syncTimeStart if syncTimeStart else get_current_date(),
        "syncTimeEnd": syncTimeEnd if syncTimeEnd else get_current_date(),
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_d5e00235-3fd3-442f-9526-ab312d40d115"
    tenant_id = 148

    async def main():
        data = await employee_sync_log(
            authorization,
            tenant_id=tenant_id)
        print(data)
    asyncio.run(main())
