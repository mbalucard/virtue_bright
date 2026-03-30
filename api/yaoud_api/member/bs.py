"""
会员信息
    - 客户信息-下拉检索用: external_member_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/member/bs"


async def external_member_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 100,
        keyword: Optional[str] = None,) -> dict:
    """
    客户信息-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 100.
        keyword (str, None): 关键字搜索. Defaults to None.
            - 支持客户名称，助记码，客户编码
    Returns:
        dict: 客户信息列表
    """
    url = f"{base_url}/external/member/pageList"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
