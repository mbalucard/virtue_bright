"""
标签管理
    - 会员标签列表-下拉检索用: item_list
    - 商品标签树-下拉检索用: goods_label_type_tree
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/labelType"

async def item_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        objType: str = "client_management") -> dict:
    """
    会员标签列表-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        objType (str, None): 对象类型.
            - (store_management:门店标签,commodity_management:商品标签,client_management:会员标签)
    Returns:
        dict: 会员标签列表
    """
    url = f"{base_url}/queryItemList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "objType": objType,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def goods_label_type_tree(
        authorization: str,
        tenant_id: Optional[int] = None,
        objType: str = "commodity_management",) -> dict:
    """
    商品标签树-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        objType (str): 对象类型.
            - (commodity_management:商品标签)
    Returns:
        dict: 商品标签树
    """
    url = f"{base_url}/queryLabelTree"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "objType": objType,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
