"""
区域管理
    - 省市区-下拉检索用: region_tree
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/region"

async def region_tree(
        authorization: str,
        tenant_id: Optional[int] = None) -> dict:
    """
    省市区-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 省市区-下拉检索用
    """
    url = f"{base_url}/queryAllRegionTreeNew"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

