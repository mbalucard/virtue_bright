"""
仓库管理
    - 仓库货位查询-下拉检索: warehouse_allocation_list
    - 仓库货位-下拉检索用: warehouse_location_list
    - 当前机构可选仓库信息-下拉检索用: select_warehouse
    - 门店仓库-下拉检索用: select_store_warehouse
    - 门店及仓库信息-下拉检索用: get_store_warehouse_list_by_enterprise_id
    - 企业及仓库查询-下拉检索用: ent_store_warehouse_query
    - 控制位置仓库及货位信息: location_control_warehouse_stores
    - 门店柜组查询-下拉检索: warehouse_cabinet_list
    - 库区查询-下拉检索: warehouse_area_list
    - 协同仓库信息-下拉检索: synergys_warehouse_info
    - 仓库管理-仓库-列表: warehouse_info_page
    - 仓库管理-仓库-详情: warehouse_info_detail
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/inventory/warehouse"


async def warehouse_allocation_list(
        authorization: str,
        warehouseIdList: List[str],
        tenant_id: Optional[int] = None,) -> dict:
    """
    仓库货位查询-下拉检索
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
    Returns:
        dict: 仓库货位查询-下拉检索响应体
    """
    url = f"{base_url}Allocation/queryWarehouseAllocation"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "warehouseIdList": warehouseIdList,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def warehouse_location_list(
        authorization: str,
        warehouseId: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    仓库货位-下拉检索用
    Args:
        authorization (str): 授权token
        warehouseId (int): 仓库ID. Defaults to None.
            - 可在 ent_store_warehouse_query 中获取 对应字段ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 仓库货位-下拉检索用
    """
    url = f"{base_url}Allocation/getList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "warehouseId": warehouseId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def select_warehouse(
        authorization: str,
        tenant_id: Optional[int] = None,
        objectType: int = 3,) -> dict:
    """
    当前机构可选仓库信息-下拉检索用
    Args:
        authorization (str): 授权token，格式为"Bearer <token>"
        tenant_id (int, None): 租户ID. Defaults to None.
        objectType (int, None): 未知参数. Defaults to 3.
    Returns:
        dict: 可选仓库信息结果
    """
    url = f"{base_url}Info/dropDownToSelectWarehouse"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "objectType": objectType,  # ? 未知参数
        "_t": timestamp()
    }

    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def select_store_warehouse(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    门店仓库-下拉检索用
    Args:
        authorization (str): 授权token，格式为"Bearer <token>"
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 门店仓库-下拉检索结果
    """
    url = f"{base_url}Info/dropDownToSelectStoreWarehouse"
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


async def get_store_warehouse_list_by_enterprise_id(
        authorization: str,
        tenant_id: Optional[int] = None,
        enterpriseId: str = None,) -> dict:
    """
    门店及仓库信息-下拉检索用
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        enterpriseId (str, None): 企业ID. Defaults to None.
    Returns:
        dict: 门店及仓库信息-下拉检索用响应体
    """
    url = f"{base_url}Info/getStoreWarehouseListByEnterpriseId"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "enterpriseId": enterpriseId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def ent_store_warehouse_query(
        authorization: str,
        tenant_id: Optional[int] = None,
        objectType: int = 3,) -> dict:
    """
    企业及仓库查询-下拉检索用
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        objectType (int, None): 未知参数. Defaults to 3.
    Returns:
        dict: 企业及仓库查询响应体
    """
    url = f"{base_url}Info/queryEnterpriseAndStoreWarehouse"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
        "objectType": objectType,
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def location_control_warehouse_stores(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    控制位置仓库及货位信息
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 控制位置仓库及货位信息响应体
    """
    url = f"{base_url}Info/locationControlWarehouseStores"
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


async def warehouse_cabinet_list(
    authorization: str,
    warehouseIdList: List[str],
    tenant_id: Optional[int] = None,) -> dict:
    """
    门店柜组查询-下拉检索
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
    Returns:
        dict: 门店柜组查询-下拉检索响应体
    """
    url = f"{base_url}Cabinet/queryWarehouseCabinet"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "warehouseIdList": warehouseIdList,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def warehouse_area_list(
    authorization: str,
    warehouseIdList: List[str],
    tenant_id: Optional[int] = None,) -> dict:
    """
    库区查询-下拉检索
    Args:
        authorization (str): 授权token
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 库区查询-下拉检索响应体
    """
    url = f"{base_url}Area/queryWarehouseArea"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "warehouseIdList": warehouseIdList,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def synergys_warehouse_info(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    协同仓库信息-下拉检索
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 仓库信息-查询响应体
    """
    url = f"{base_url}Info/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {}
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def warehouse_info_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    keyWord: Optional[str] = None,
    status: Optional[int] = None,)->dict:
    """
    仓库管理-仓库-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        keyWord (str, None): 关键字. Defaults to None.
            - 支持仓库名称 仓库编码 助记码
        status (int, None): 仓库状态. Defaults to None.
            - 0-启用 1-禁用
    Returns:
        dict: 仓库管理-仓库-列表
    """
    url = f"{base_url}Info/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyWord": keyWord,
        "status": status,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def warehouse_info_detail(
    authorization: str,
    id: int,
    tenant_id: Optional[int] = None,)->dict:
    """
    仓库管理-仓库-详情
    Args:
        authorization (str): 认证信息
        id (int): 仓库ID.
            -可在 warehouse_info_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 仓库管理-仓库-详情
    """
    url = f"{base_url}Info/getDetailById/{id}"
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

