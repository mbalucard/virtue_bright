"""
系统管理
    - 切换到租户切换页: switch_owner_page
    - 切换机构: switch_organ
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/system"

async def switch_owner_page(authorization: str) -> dict:
    """
    切换到租户切换页
    Args:
        authorization (str): 认证信息
    Returns:
        dict: 是否切换成功，bool
    """
    url = f"{base_url}/switchOwnerPage"
    params = {"_t": timestamp()}
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "skipToken": "true",
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    return response.json()


async def switch_organ(authorization: str, organ_id: int) -> dict:
    """
    切换机构
    Args:
        authorization (str): 认证信息
        organ_id (int): 机构ID
    Returns:
        dict: 切换机构结果
    """
    url = f"{base_url}/switchOrgan"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
    }
    params = {
        "id": organ_id,
        "mac": "",
        "forceRestriction": "true",
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    return response.json()
