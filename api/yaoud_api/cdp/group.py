"""
会员权益组
    - 会员权益组列表-下拉检索用: get_member_group_list
    - 会员权益组列表: member_group_list
    - 会员权益组详情: member_group_details
"""


from httpx import AsyncClient
from typing import Optional

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time,timestamp


base_url = f"{yaoud_env['url']}/cdp/group"

async def get_member_group_list(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    会员权益组列表-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员权益组列表
    """
    url = f"{base_url}/getGroupList"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def member_group_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    storeCode: Optional[str] = None,) -> dict:
    """
    会员权益组列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        storeCode (str, None): 门店编码. Defaults to None.
            - 可在 get_common_organ_by_type 中获取.
    Returns:
        dict: 会员权益组列表
    """
    url = f"{base_url}/groupPage"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "storeCode": storeCode,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def member_group_details(
    authorization: str,
    id: int,
    tenant_id: Optional[int] = None,)->dict:
    """
    会员权益组详情
    Args:
        authorization (str): 认证信息
        id (int): 会员权益组ID.
            - 可在 member_group_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员权益组详情
    """
    url = f"{base_url}/selectGroupById"
    headers = {
        "authorization": authorization,
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