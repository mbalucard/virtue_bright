"""
登录账户
    - 获取所有版本信息: get_all_edition
    - 获取可切换租户及企业列表: home_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/loginAccount"


async def get_all_edition(authorization: str) -> dict:
    """
    获取所有版本信息
    Args:
        authorization (str): 认证信息
    Returns:
        dict: 所有版本信息
    """
    url = f"{base_url}/getAllEdition"
    params = {"_t": timestamp()}
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "skipToken": "true",
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    return response.json()

async def home_page(authorization: str) -> dict:
    """
    获取可切换租户及企业列表
    - 若需查询所有可切换企业，需先执行switch_owner_page
    Args:
        authorization (str): 认证信息
    Returns:
        dict: 可切换租户及企业列表
    """
    url = f"{base_url}/tenantIndex/homepage"
    params = {"_t": timestamp()}
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "skipToken": "true",
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    return response.json()
