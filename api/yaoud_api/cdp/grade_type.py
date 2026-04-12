"""
会员等级类型
    - 会员等级类型列表: member_grade_type
"""

from httpx import AsyncClient
from typing import Optional

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time,timestamp


base_url = f"{yaoud_env['url']}/cdp/gradeType"
TTL = yaoud_env["timeout"]

async def member_grade_type(
    authorization: str,
    groupId: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    会员等级类型列表
    Args:
        authorization (str): 认证信息
        groupId (str): 会员权益组ID. 
            -可在 get_member_group_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员等级类型列表
    """
    url = f"{base_url}/list"
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