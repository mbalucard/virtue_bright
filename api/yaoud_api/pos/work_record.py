"""
交班记录
    - 交班记录: work_record
    - 交班记录-摘要: work_record_summary
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/pos/workRecord"
TTL = yaoud_env["timeout"]


async def work_record(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        workTimeStart: Optional[str] = None,
        workTimeEnd: Optional[str] = None,
        brId: Optional[int] = None,
        cashierId: Optional[int] = None,
        workNo: Optional[str] = None,) -> dict:
    """
    交班记录
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        workTimeStart (str,None): 交班开始时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        workTimeEnd (str,None): 交班结束时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        brId (int,None): 门店编码. Defaults to None.
        cashierId (int,None): 人员ID. Defaults to None.
        workNo (str,None): 班次名称. Defaults to None.
    Returns:
        dict: 交班记录
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if workTimeStart:
        work_time_start = get_date_start_and_end_time(workTimeStart)
    else:
        taday = get_current_date()
        work_time_start = get_date_start_and_end_time(taday)
    if workTimeEnd:
        work_time_end = get_date_start_and_end_time(workTimeEnd)
    else:
        work_time_end = None
    params = {
        "current": current,
        "size": size,
        "workTimeStart": work_time_start['start_time'] if work_time_start else None,
        "workTimeEnd": work_time_end['end_time'] if work_time_end else None,
        "brId": brId,
        "cashierId": cashierId,
        "workNo": workNo,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def work_record_summary(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        workTimeStart: Optional[str] = None,
        workTimeEnd: Optional[str] = None,
        brId: Optional[int] = None,
        cashierId: Optional[int] = None,
        workNo: Optional[str] = None,) -> dict:
    """
    交班记录-摘要
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        workTimeStart (str,None): 交班开始时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        workTimeEnd (str,None): 交班结束时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        brId (int,None): 门店编码. Defaults to None.
        cashierId (int,None): 人员ID. Defaults to None.
        workNo (str,None): 班次名称. Defaults to None.
    Returns:
        dict: 交班记录-摘要
    """
    url = f"{base_url}/summary"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if workTimeStart:
        work_time_start = get_date_start_and_end_time(workTimeStart)
    else:
        taday = get_current_date()
        work_time_start = get_date_start_and_end_time(taday)
    if workTimeEnd:
        work_time_end = get_date_start_and_end_time(workTimeEnd)
    else:
        work_time_end = None
    params = {
        "current": current,
        "size": size,
        "workTimeStart": work_time_start['start_time'] if work_time_start else None,
        "workTimeEnd": work_time_end['end_time'] if work_time_end else None,
        "brId": brId,
        "cashierId": cashierId,
        "workNo": workNo,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
