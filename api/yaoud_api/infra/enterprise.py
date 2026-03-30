"""
企业管理
    - 企业管理-企业列表: enterprise_page
    - 企业管理-企业详情: enterprise_detail
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/enterprise"

async def enterprise_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 100,
    withParam: Optional[str] = None,
    shopStatus: Optional[int] = None,
    goodTypeList: Optional[List[str]] = None,)->dict:
    """
    企业管理-企业列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 100.
        withParam (str, None): 关键字. Defaults to None.
        shopStatus (int, None): 企业状态. Defaults to None.
            - 1-启用 0-禁用
        goodTypeList (list[str], None): 业务类型. Defaults to None.
            -可在 dict_item_list 中获取 keyword="商品类型"
    Returns:
        dict: 企业管理-企业列表
    """
    url = f"{base_url}/enterprisePage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "withParam": withParam,
        "shopStatus": shopStatus,
        "goodTypeList": goodTypeList,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def enterprise_detail(
    authorization: str,
    id: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    企业管理-企业详情
    Args:
        authorization (str): 认证信息
        id (int): 企业ID.
            -可在 enterprise_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 企业管理-企业详情
    """
    url = f"{base_url}/getEnterpriseById"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
