"""
基础信息
    - 经营范围树-下拉检索用: business_scope_tree_list
    - 生产范围树-下拉检索用: production_scope_tree
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/base"

async def business_scope_tree_list(
    authorization: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    经营范围树-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 经营范围树
    """
    url = f"{base_url}/data/businessScope/treeList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def production_scope_tree(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    生产范围树-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 生产范围树
    """
    url = f"{base_url}/data/productionScope/treeList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
