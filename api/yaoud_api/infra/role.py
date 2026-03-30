"""
角色管理
    - 获取模块列表或节点树: get_block_enterprise_tree
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/role"

async def get_block_enterprise_tree(
        authorization: str,
        systemType: int = 2,
        tenant_id: Optional[int] = None,) -> dict:
    """
    获取模块列表或节点树
    Args:
        authorization (str): 认证信息
        systemType (int): 系统类型. Defaults to 2.
            - 1: 模块列表
            - 2: 节点树
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 模块列表或节点树
    """
    url = f"{base_url}/getBlocEnterpriseTree"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "systemType": systemType,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

    