"""
机构信息
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/organ"


async def get_common_organ_by_type(
        authorization: str,
        tenant_id: Optional[int] = None,
        type: int = 3,
        current: int = 1,
        size: int = 100,
        enterpriseId: Optional[int] = None,) -> dict:
    """
    获取门店信息-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        type (int): 类型. Defaults to 3.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 100.
        enterpriseId (int, None): 企业ID. Defaults to None.
    """
    url = f"{base_url}/getCommonOrganByType"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "type": type,
        "enterpriseId": enterpriseId,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
