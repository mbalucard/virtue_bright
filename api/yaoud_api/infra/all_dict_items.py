"""
字典管理
    - 所有字典项: all_dict_items
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/infra/dict"

async def all_dict_items(
    authorization: str,
    tenant_id: Optional[int] = None,
)->dict:
    """
    所有字典项
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 所有字典项
    """
    url = f"{base_url}/queryAllDictItemsForTenant"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_2523d693-9265-4016-a6e3-e34f5a5dff90"
    tenant_id = 148
    data = asyncio.run(all_dict_items(authorization, tenant_id))
    print(data["data"]['D107-007'])