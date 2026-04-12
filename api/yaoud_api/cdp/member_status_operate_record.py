"""
会员状态操作记录
    - 会员冻结列表: member_freeze_list
    - 会员注销列表: member_cancel_list
"""

from httpx import AsyncClient
from typing import Optional

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time,timestamp



base_url = f"{yaoud_env['url']}/cdp/memberStatusOperateRecord"


async def member_freeze_list(
        authorization: str,
        groupId: int,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        gradeId: Optional[str] = None,
        status: Optional[int] = None,
        freezeOperator: Optional[str] = None,
        freezeTimeBegin: Optional[str] = None,
        freezeTimeEnd: Optional[str] = None,
        unfreezeTimeBegin: Optional[str] = None,
        unfreezeTimeEnd: Optional[str] = None,) -> dict:
    """
    会员冻结列表
    Args:
        authorization (str): 认证信息
        groupId (int): 会员权益组id
            - 可在 get_member_group_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str, None): 关键字搜索. Defaults to None.
            - 支持会员名称，手机号，会员卡号
        gradeId (str, None): 会员组分级 ID. Defaults to None.
            - 可在 get_grade_by_group_id 中获取.
        status (int, None): 冻结状态. Defaults to None.
            - (1:已冻结, 3:已解冻)
        freezeOperator (str, None): 冻结操作人. Defaults to None.
        freezeTimeBegin (str, None): 冻结检索开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        freezeTimeEnd (str, None): 冻结检索结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        unfreezeTimeBegin (str, None): 解冻检索开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        unfreezeTimeEnd (str, None): 解冻检索结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 会员冻结列表
    """
    url = f"{base_url}/getFreezePage"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if freezeTimeBegin:
        freezeTimeBegin = get_date_start_and_end_time(freezeTimeBegin)
    if freezeTimeEnd:
        freezeTimeEnd = get_date_start_and_end_time(freezeTimeEnd)
    if unfreezeTimeBegin:
        unfreezeTimeBegin = get_date_start_and_end_time(unfreezeTimeBegin)
    if unfreezeTimeEnd:
        unfreezeTimeEnd = get_date_start_and_end_time(unfreezeTimeEnd)

    payload = {
        "current": current,
        "size": size,
        "groupId": groupId,
        "keyword": keyword,
        "gradeId": gradeId,
        "status": status,
        "freezeOperator": freezeOperator,
        "freezeTimeBegin": freezeTimeBegin['start_time'] if freezeTimeBegin else None,
        "freezeTimeEnd": freezeTimeEnd['end_time'] if freezeTimeEnd else None,
        "unfreezeTimeBegin": unfreezeTimeBegin['start_time'] if unfreezeTimeBegin else None,
        "unfreezeTimeEnd": unfreezeTimeEnd['end_time'] if unfreezeTimeEnd else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def member_cancel_list(
        authorization: str,
        groupId: int,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        gradeId: Optional[str] = None,
        status: Optional[int] = None,
        freezeOperator: Optional[str] = None,
        freezeTimeBegin: Optional[str] = None,
        freezeTimeEnd: Optional[str] = None,
        unfreezeTimeBegin: Optional[str] = None,
        unfreezeTimeEnd: Optional[str] = None,) -> dict:
    """
    会员注销列表
    Args:
        authorization (str): 认证信息
        groupId (int): 会员权益组id
            - 可在 get_member_group_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str, None): 关键字搜索. Defaults to None.
            - 支持会员名称，手机号，会员卡号
        gradeId (str, None): 会员组分级 ID. Defaults to None.
            - 可在 get_grade_by_group_id 中获取.
        status (int, None): 注销状态. Defaults to None.
            - 5:注销中 7:已注销 9:已撤销
        freezeOperator (str, None): 注销操作人. Defaults to None.
        freezeTimeBegin (str, None): 注销检索时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        freezeTimeEnd (str, None): 注销检索时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        unfreezeTimeBegin (str, None): 注销成功/撤销成功检索时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        unfreezeTimeEnd (str, None): 注销成功/撤销成功检索时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}/getCancelPage"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if freezeTimeBegin:
        freezeTimeBegin = get_date_start_and_end_time(freezeTimeBegin)
    if freezeTimeEnd:
        freezeTimeEnd = get_date_start_and_end_time(freezeTimeEnd)
    if unfreezeTimeBegin:
        unfreezeTimeBegin = get_date_start_and_end_time(unfreezeTimeBegin)
    if unfreezeTimeEnd:
        unfreezeTimeEnd = get_date_start_and_end_time(unfreezeTimeEnd)

    payload = {
        "current": current,
        "size": size,
        "groupId": groupId,
        "keyword": keyword,
        "gradeId": gradeId,
        "status": status,
        "freezeOperator": freezeOperator,
        "freezeTimeBegin": freezeTimeBegin['start_time'] if freezeTimeBegin else None,
        "freezeTimeEnd": freezeTimeEnd['end_time'] if freezeTimeEnd else None,
        "unfreezeTimeBegin": unfreezeTimeBegin['start_time'] if unfreezeTimeBegin else None,
        "unfreezeTimeEnd": unfreezeTimeEnd['end_time'] if unfreezeTimeEnd else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
