"""
门店信息
    - 可用门店信息-下拉检索用-已启用: available_institutions_list
    - 门店信息-下拉检索用-全部门店: common_organ_of_login_page_of_status
    - 按医保查询门店-下拉检索用: medical_insurance_ent
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/shopinfo"


async def available_institutions_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    可用门店信息-下拉检索用-已启用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 关键字检索. Defaults to None.
            - 可查询门店简称，门店编码，助记码
    Returns:
        dict: 可用门店信息
    """
    url = f"{base_url}/getCommonOrganOfLogin"
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

async def common_organ_of_login_page_of_status(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,
        current: int = 1,
        size: int = 100,) -> dict:
    """
    门店信息-下拉检索用-全部门店
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 关键字检索. Defaults to None.
            - 可查询门店简称，门店编码，助记码
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 100.
    Returns:
        dict: 门店信息
    """
    url = f"{base_url}/getCommonOrganOfLoginPageOfStatus"
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

async def medical_insurance_ent(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,)->dict:
    """
    按医保查询门店-下拉检索用
    包含医保区化码
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 关键字检索. Defaults to None.
            - 门店名称 门店简称 门店编码
    Returns:
        dict: 按医保查询门店-下拉检索用
    """
    url = f"{base_url}/getMiByEnterprise"
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

