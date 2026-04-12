"""
门店管理
    - 门店信息查询: shop_info_page
    - 门店信息查询-详情: shop_info_detail
    - 获取门店列表-下拉检索用-全部门店: get_stores
    - 门店信息-下拉检索用-所有门店: select_stores
    - 门店信息查询-下拉检索用: get_store_list
    - 门店区域树: store_region_tree
    - 班次信息查询-下拉检索用: shift_param_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/stores"


async def shop_info_page(
        authorization: str,
        parentId: Optional[int] = None,
        tenant_id: Optional[int] = None,
        withParam: Optional[str] = None,
        current: int = 1,
        size: int = 20,
        shopStatus: Optional[int] = None,
        shopType: Optional[int] = None,
        isRegionDirectly: bool = False,
        goodTypeList: Optional[List[str]] = None):
    """
    门店信息查询
    Args:
        authorization (str): 认证信息
        parentId (int,None): 父级id.默认None，则查询所有门店. Defaults to None.
            -可在 store_region_tree 中获取。
        tenant_id (int, None): 租户ID. Defaults to None.
        withParam (str, None): 检索参数. Defaults to None.
            - 支持门店名称，门店编码，助记码
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        shopStatus (int, None): 门店状态. Defaults to None.
            - (1:启用，0:停业)
        shopType (int, None): 门店类型(1:直营，2:加盟). Defaults to None.
            - (1:直营，2:加盟)
        isRegionDirectly (bool): 只显示区域直属门店. Defaults to False.
        goodTypeList (List[str], None): 主营商品类型列表. Defaults to None.
            -可在 dict_item_list 中获取 keyword="商品类型".
    Returns:
        dict: 门店信息
    """
    url = f"{base_url}/shopInfoPage"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,  # 当前页
        "size": size,  # 每页条目数最大100
        "withParam": withParam,  # 检索参数，门店名称，门店编码，助记码
        "parentId": parentId,  # 父级id
        "type": 3,
        "shopStatus": shopStatus,  # 门店状态，(1:启用，0:停业)
        "shopType": shopType,  # 门店类型(1:直营，2:加盟)
        "isRegionDirectly": isRegionDirectly,  # 只显示区域直属门店
        "goodTypeList": goodTypeList,  # 商品类型列表
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    return response.json()


async def shop_info_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    门店信息查询-详情
    Args:
        authorization (str): 认证信息
        id (int): 门店ID
            -可在 shop_info_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 门店信息
    """
    url = f"{base_url}/getShopInfoById"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def get_stores(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,
        current: int = 1,
        size: int = 100,) -> dict:
    """
    获取门店列表-下拉检索用-全部门店
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 关键字检索. Defaults to None.
            - 可查询门店简称，门店编码，门店名称
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 100.
    Returns:
        dict: 门店列表
    """
    url = f"{base_url}/getStoresPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def select_stores(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    门店信息-下拉检索用-所有门店
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 门店信息
    """
    url = f"{base_url}/dropDownToSelectStores"
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

async def get_store_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    keyword: Optional[str] = None,) -> dict:
    """
    门店信息查询-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 关键字检索. Defaults to None.
            - 支持门店名称，门店编码
    Returns:
        dict: 门店信息列表
    """
    url = f"{base_url}/queryStoresByCodeOrName"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "keyword": keyword,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def store_region_tree(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    门店区域树
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 门店区域树
    """
    url = f"{base_url}/queryRegionTree"
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


async def shift_param_list(
        authorization: str,
        enterpriseId: Optional[int] = None,
        tenant_id: Optional[int] = None,) -> dict:
    """
    班次信息查询-下拉检索用
    Args:
        authorization (str): 认证信息
        enterpriseId (int, None): 企业ID.
            - 若为None，则查询当前企业所有班次. Defaults to None.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 班次信息
    """
    url = f"{base_url}/param/schedule/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        # ! enterpriseId若有之，查询永远是AB班，只是ID不一样，不知道干什么用的
        "enterpriseId": enterpriseId,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    return response.json()
