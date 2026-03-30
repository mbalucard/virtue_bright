"""
店铺配置
    - 店铺信息-下拉检索用: shop_config_page_list
    - 店铺类型信息-下拉检索用: shop_config_desc_list
    - 业务类型信息-下拉检索用: shop_config_type_list
    - 店铺信息查询: shop_config_page_list_new
    - 店铺信息-详情: shop_config_detail
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/shopProduct/rlShopConfig"


async def shop_config_page_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        shopStatus: Optional[int] = None,
        keyword: Optional[str] = None,
        categorie: Optional[int] = None,) -> dict:
    """
    店铺信息-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数，-1为全部. Defaults to 20.
        shopStatus (int, None): 店铺状态. Defaults to None.
            - 0:已禁用
            - 1:已启用
        keyword (str, None): 关键字搜索. Defaults to None.
            - 支持模糊查找，可查询店铺编码，店铺名称
        categorie (int, None): 店铺类型编码. Defaults to None.
            - 可在 shop_config_desc_list 中获取
    Returns:
        dict: 店铺信息
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "shopStatus": shopStatus,
        "keyword": keyword if keyword else "",
        "type": categorie,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def shop_config_desc_list(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    店铺类型信息-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 店铺类型信息
    """
    url = f"{base_url}/descList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def shop_config_type_list(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    业务类型信息-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 业务类型信息
    """
    url = f"{base_url}/typeList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def shop_config_page_list_new(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        shopStatus: Optional[int] = None,
        keyword: Optional[str] = None,
        isMatch: Optional[int] = None,
        typeList: Optional[List[str]] = None,
        typeSonList: Optional[List[int]] = None,
        enterpriseId: Optional[int] = None,
        storeId: Optional[int] = None,) -> dict:
    """
    店铺信息查询
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        shopStatus (int, None): 店铺状态. Defaults to None.
            - 0:已禁用
            - 1:已启用
        keyword (str, None): 关键字搜索. Defaults to None.
            - 支持模糊查找，可查询店铺编码，店铺名称
        isMatch (int, None): 授权状态. Defaults to None.
            - 0:待授权
            - 1:已授权
            - 2:无需授权
            - 3:已失效
        typeList (List[str], None): 业务类型， Defaults to None.
            -可在 shop_config_type_list 中获取.
        typeSonList (List[int], None): 店铺类型，Defaults to None.
            -可在 shop_config_desc_list 中获取.
        enterpriseId (int, None): 企业ID. Defaults to None.
            - 若果storeID不为空，则此参数无效.
        storeId (int, None): 门店ID. Defaults to None.
    Returns:
        dict: 店铺信息
    """
    url = f"{base_url}/pageListNew"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "shopStatus": shopStatus,
        "keyword": keyword if keyword else "",
        "isMatch": isMatch,
        "typeList": typeList,
        "typeSonList": typeSonList,
        "enterpriseId": enterpriseId,
        "storeId": storeId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def shop_config_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    店铺信息-详情
    Args:
        authorization (str): 认证信息
        id (int): 店铺ID.
            -可在 shop_config_page_list_new 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 店铺信息-详情
    """
    url = f"{base_url}/getShopConfigById/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
