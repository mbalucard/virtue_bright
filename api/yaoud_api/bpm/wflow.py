"""
工作流
    - 审批流程进度: instance_progress
    - 审批流单据导航-字段显示配置: wflow_init_show_field_detail
    - 审批流单据导航: wflow_task_navigation
    - 审批任务-待办列表: wflow_task_todo_list
    - 审批任务-已办列表: wflow_task_ido_list
    - 审批任务-已发起: wflow_process_my_submitted
"""


from httpx import AsyncClient
from typing import Optional

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_date_start_and_end_time, get_current_date,retrieve_past_date


base_url = f"{yaoud_env['url']}/bpm/wflow"


async def instance_progress(
        authorization: str,
        id: str,
        code: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    审批流程进度
    Args:
        authorization (str): 授权token
        id (str): 实例ID.
        code (str): 单据编码
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 审批流程进度
    """
    url = f"{base_url}/process/instanceProgress/{id}/{code}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def wflow_init_show_field_detail(
        authorization: str,
        businessType: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    审批流单据导航-字段显示配置
    Args:
        authorization (str): 认证信息
        businessType (int): 业务类型
            - 可在 wflow_task_navigation 中获取 对应字段: businessType
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 审批流单据导航-字段显示配置
    """
    url = f"{base_url}/init/showFieldDetail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "businessType": businessType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def wflow_task_navigation(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    审批流单据导航
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 审批流单据导航
    """
    url = f"{base_url}/process/task/navigation"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {}
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def wflow_task_todo_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        orderId: Optional[str] = None,
        createUserId: Optional[str] = None,
        systemId: Optional[int] = None,
        moduleCode: Optional[str] = None,
        formName: Optional[str] = None,
        key: Optional[str] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        loginEnterprise: str = "false",) -> dict:
    """
    审批任务-待办列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str, None): 审批名称. Defaults to None.
        orderId (str, None): 审批单号. Defaults to None.
        createUserId (str, None): 发起人ID. Defaults to None.
            - 可在 get_employee_list 接口获取
        systemId (int, None): 系统ID. Defaults to None.
            - 可在 wflow_task_navigation 中获取
        moduleCode (str, None): 模块编码. Defaults to None.
            - 可在 wflow_task_navigation 中获取
        formName (str, None): 表单名称. Defaults to None.
            - 可在 wflow_task_navigation 中获取 businessType 字段
        key (str, None):  Defaults to None.
            - #! 用途不明，和 formName 字段一样
        createStartTime (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createEndTime (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        loginEnterprise (str): 是否仅看当前登录企业. Defaults to "false".
            - true-是 false-否
    Returns:
        dict: 审批任务-待办列表
    """

    url = f"{base_url}/process/task/todoList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createStartTime:
        createStartTime = get_date_start_and_end_time(createStartTime)
    if createEndTime:
        createEndTime = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        createEndTime = get_date_start_and_end_time(taday)
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "orderId": orderId,
        "createUserId": createUserId,
        "systemId": systemId,
        "moduleCode": moduleCode,
        "formName": formName,
        "key": key if key else formName,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "loginEnterprise": loginEnterprise,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def wflow_task_ido_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    keyword: Optional[str] = None,
    orderId: Optional[str] = None,
    organName: Optional[str] = None,
    result: Optional[str] = None,
    createUserId: Optional[str] = None,
    systemId: Optional[int] = None,
    moduleCode: Optional[str] = None,
    formName: Optional[str] = None,
    key: Optional[str] = None,
    loginEnterprise: str = "false",
    createStartTime: Optional[str] = None,
    createEndTime: Optional[str] = None,
    showMine: int = 0,) -> dict:
    """
    审批任务-已办列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str, None): 审批名称. Defaults to None.
        orderId (str, None): 审批单号. Defaults to None.
        organName (str, None): 发起登陆机构. Defaults to None.
        result (str, None): 审批状态. Defaults to None.
            - in-approval-审批中, process-end-已审批 refuse-end-驳回 cancel-end-已撤销
        createUserId (str, None): 发起人ID. Defaults to None.
            - 可在 get_employee_list 接口获取
        systemId (int, None): 系统ID. Defaults to None.
            - 可在 wflow_task_navigation 中获取
        moduleCode (str, None): 模块编码. Defaults to None.
            - 可在 wflow_task_navigation 中获取
        formName (str, None): 表单名称. Defaults to None.
            - 可在 wflow_task_navigation 中获取 businessType 字段
        key (str, None):  Defaults to None.
            - #! 用途不明，和 formName 字段一样
        loginEnterprise (str): 是否仅看当前登录企业. Defaults to "false".
            - true-是 false-否
        showMine (int): 是否仅看我的. Defaults to 0.
            - 0-否 1-是
        createStartTime (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createEndTime (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    Returns:
        dict: 审批任务-已办列表
    """
    url = f"{base_url}/process/task/idoList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createStartTime:
        createStartTime = get_date_start_and_end_time(createStartTime)
    elif createEndTime and not createStartTime:
        createStartTime = get_date_start_and_end_time(createEndTime)
    else:
        day = retrieve_past_date(days_ago=30)
        createStartTime = get_date_start_and_end_time(day)
    if createEndTime:
        createEndTime = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        createEndTime = get_date_start_and_end_time(taday)
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "orderId": orderId,
        "organName": organName,
        "result": result,
        "createUserId": createUserId,
        "systemId": systemId,
        "moduleCode": moduleCode,
        "formName": formName,
        "key": key if key else formName,
        "loginEnterprise": loginEnterprise,
        "showMine": showMine,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def wflow_process_my_submitted(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    keyword: Optional[str] = None,
    orderId: Optional[str] = None,
    result: Optional[str] = None,
    createUserId: Optional[str] = None,
    systemId: Optional[int] = None,
    moduleCode: Optional[str] = None,
    formName: Optional[str] = None,
    key: Optional[str] = None,
    loginEnterprise: str = "false",
    createStartTime: Optional[str] = None,
    createEndTime: Optional[str] = None,) -> dict:
    """
    审批任务-已发起
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str, None): 审批名称. Defaults to None.
        orderId (str, None): 审批单号. Defaults to None.
        result (str, None): 审批状态. Defaults to None.
            - in-approval-审批中, process-end-已审批 refuse-end-驳回 cancel-end-已撤销
        createUserId (str, None): 发起人ID. Defaults to None.
            - 可在 get_employee_list 接口获取
        systemId (int, None): 系统ID. Defaults to None.
            - 可在 wflow_task_navigation 中获取
        moduleCode (str, None): 模块编码. Defaults to None.
            - 可在 wflow_task_navigation 中获取
        formName (str, None): 表单名称. Defaults to None.
            - 可在 wflow_task_navigation 中获取 businessType 字段
        key (str, None):  Defaults to None.
            - #! 用途不明，和 formName 字段一样
        loginEnterprise (str): 是否仅看当前登录企业. Defaults to "false".
            - true-是 false-否
        createStartTime (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createEndTime (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    Returns:
        dict: 审批任务-已发起
    """
    url = f"{base_url}/process/mySubmitted"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createStartTime:
        createStartTime = get_date_start_and_end_time(createStartTime)
    if createEndTime:
        createEndTime = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        createEndTime = get_date_start_and_end_time(taday)

    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "orderId": orderId,
        "result": result,
        "createUserId": createUserId,
        "systemId": systemId,
        "moduleCode": moduleCode,
        "formName": formName,
        "key": key if key else formName,
        "loginEnterprise": loginEnterprise,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
