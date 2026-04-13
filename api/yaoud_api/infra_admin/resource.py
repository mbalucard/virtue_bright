"""
资源管理
    - 资源树-列表: resource_tree_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/infraAdmin/resource"
TTL = yaoud_env["timeout"]


async def resource_tree_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        parent_id: Optional[int] = None,) -> dict:
    """
    资源树-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        parent_id (int, None): 父级ID. Defaults to None.
            - 虽然接口参数是parentCode, 但是实际查询时是parentId, 可以用 6806 验证
    Returns:
        dict: 资源树-列表
    """
    url = f"{base_url}/treeList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        # "parentCode": parent_id,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_e989f1a7-81ea-453e-b282-f0e79a3494af"
    tenant_id = 148
    parent_id = None

    async def main():
        data = await resource_tree_list(authorization, tenant_id, parent_id)
        print(data)
    asyncio.run(main())
