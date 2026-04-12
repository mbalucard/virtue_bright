"""
企业微信-员工管理
    - 企业微信-员工列表: external_user_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/external/user"
TTL = yaoud_env["timeout"]

async def external_user_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyWord: Optional[str] = None,) -> dict:
    """
    企业微信-员工列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        keyWord (str, None): 关键字搜索. Defaults to None.
            - 支持检索员工名称,手机号
    Returns:
        dict: 企业微信员工列表
    """
    url = f"{base_url}/getPage"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    parames = {
        "current": current,
        "size": size,
        "keyWord": keyWord,
        "_t": timestamp(),
    }

    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=parames, timeout=TTL)
    return response.json()

