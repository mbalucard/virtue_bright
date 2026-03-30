"""
企业微信-外部联系人
    - 企业微信-好友列表: external_contact
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/external/externalcontact"



async def external_contact(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyWord: Optional[str] = None,
        bindingStatus: Optional[int] = None,
        statusType: Optional[int] = None,
        userId: Optional[int] = None,
        startJoinTime: Optional[str] = None,
        endJoinTime: Optional[str] = None,) -> dict:
    """
    企业微信-好友列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyWord (str, None): 关键字搜索. Defaults to None.
            - 支持检索微信昵称，企微备注名，绑定会员名称
        bindingStatus (int, None): 绑定状态. Defaults to None.
            - (1:已绑定, 0:未绑定)
        statusType (int, None): 好友状态. Defaults to None.
            - (1:正常，2:员工删除客户，3:客户删除员工)
        userId (int, None): 所属员工ID.
            - 可在external_user_list中的bindEmpId字段找到
        startJoinTime (str, None): 添加时间开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        endJoinTime (str, None): 添加时间结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 企业微信好友列表
    """
    url = f"{base_url}/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if startJoinTime:
        startJoinTime = get_date_start_and_end_time(startJoinTime)
    if endJoinTime:
        endJoinTime = get_date_start_and_end_time(endJoinTime)

    payload = {
        "current": current,
        "size": size,
        "keyWord": keyWord,
        "bindingStatus": bindingStatus,
        "statusType": statusType,
        "userId": userId,
        "startJoinTime": startJoinTime['start_time'] if startJoinTime else None,
        "endJoinTime": endJoinTime['end_time'] if endJoinTime else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

