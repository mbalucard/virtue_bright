"""
企业微信群
    - 企业微信群列表: group_chat_list
    - 企业微信群成员列表: group_chat_user_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/external/groupChat"


async def group_chat_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,) -> dict:
    """
    企业微信-群列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, optional): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str,None): 关键字搜索. Defaults to None.
            - 支持群名称，群主名称，群管理员名称
    Returns:
        dict: 企业微信群列表
    """
    url = f"{base_url}/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])

    return response.json()


async def group_chat_user_list(
        authorization: str,
        chat_id: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,) -> dict:
    """
    企业微信-群成员列表
    Args:
        authorization (str): 认证信息
        chat_id (str): 企业微信群ID.
            - 可在 group_chat_list 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyword (str,None): 关键字搜索. Defaults to None.
            - 支持群成员名称,客户昵称，邀请人名称
    Returns:
        dict: 企业微信群成员列表
    """
    url = f"{base_url}RhUser/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "chatId": chat_id,
        "keyword": keyword,
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    return response.json()

