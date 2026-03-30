"""
报告数据
    - 仓库信息列表: warehouse_info_list
"""


from httpx import AsyncClient
from typing import Optional

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp


base_url = f"{yaoud_env['url']}/bi/report"


async def warehouse_info_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    keyword: Optional[str] = None,
    current: int = 1,
    size: int = 100,
) -> dict:
    """
    仓库信息列表(已启用机构的仓库，含门店及总部仓库)
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 搜索关键字. Defaults to None.
            - 支持模糊查找，可搜索企业名称，助记码，企业简称，企业编码
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 100.
    Returns:
        dict: 仓库信息列表响应体
    """
    url = f"{base_url}/listDcAndStoInfo"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()