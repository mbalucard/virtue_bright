"""
会员注册
    - 会员注册设置: member_register_config
"""

from httpx import AsyncClient
from typing import Optional

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time,timestamp


base_url = f"{yaoud_env['url']}/cdp/memberRegisterConfig"

async def member_register_config(
    authorization: str,
    groupId: int,
    clientType: int = 0,
    tenant_id: Optional[int] = None,) -> dict:
    """
    会员注册设置
    Args:
        authorization (str): 认证信息
        groupId (int): 会员权益组ID. 
            -可在 get_member_group_list 中获取.
        clientType (int): 客户端类型. Defaults to 0.
            -0-pos收银及员工小程序 
            -1-会员小程序
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员注册设置
    """
    url = f"{base_url}/list"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "groupId": groupId,
        "clientType": clientType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
