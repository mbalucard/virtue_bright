"""
组合商品
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/shopProduct/rlGroupProduct"

async def group_product_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        groupType: Optional[int] = None,
        keyword: Optional[str] = None,
        baseKeyWord: Optional[str] = None,) -> dict:
    """
    零售价格组-组合商品管理
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        groupType (int, None): 组合类型. Defaults to None.
            - 1-单品组合
            - 2-多品组合
        keyword (str, None): 组合商品名称或编码. Defaults to None.
            - 支持模糊查询
        baseKeyWord (str, None): 商品名称或编码. Defaults to None.
            - 支持模糊查询
    Returns:
        dict: 零售价格组-组合商品管理
    """
    url = f"{base_url}/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "groupType": groupType,
        "keyword": keyword,  # ! keyword 检索内容包含 baseKeyWord 的效果.
        "baseKeyWord": baseKeyWord,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def group_product_detail(
    authorization: str,
    id: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    零售价格组-组合商品管理-详情
    Args:
        authorization (str): 认证信息
        id (int): 组合商品ID. 可在 group_product_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 零售价格组-组合商品管理-详情
    """
    url = f"{base_url}/getGroupProductDetail/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
