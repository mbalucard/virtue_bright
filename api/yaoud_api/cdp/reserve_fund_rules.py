"""
会员储值金规则
    - 会员资产设置-储值金规则: reserve_fund_rules
"""

from httpx import AsyncClient
from typing import Optional

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time,timestamp


base_url = f"{yaoud_env['url']}/cdp/reserveFundRules"
TTL = yaoud_env["timeout"]

async def reserve_fund_rules(
    authorization: str,
    groupId: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    会员资产设置-储值金规则
    Args:
        authorization (str): 认证信息
        groupId (int): 会员权益组ID. 
            -可在 get_member_group_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 储值金规则
    """
    url = f"{base_url}/getReserveFundRules"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "groupId": groupId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
