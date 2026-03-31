"""
职位管理
    - 职位分类列表: position_classification_page
    - 职位等级列表: position_level_page
    - 职位列表: position_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrPosition"


async def position_classification_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    classificationStatus: Optional[int] = None,) -> dict:
    """
    职位分类列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - 支持名称，编码
        classificationStatus (int, None): 是否启用. Defaults to None.
    Returns:
        dict: 职位分类列表
    """
    url = f"{base_url}/classification/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "classificationStatus": classificationStatus,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def position_level_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    positionLevelStatus: Optional[int] = None,) -> dict:
    """
    职位等级列表
    #! 咱无数据，未测试具体效果
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - 支持名称,编码
        positionLevelStatus (int, None): 是否启用. Defaults to None.
            - 0: 禁用 1: 启用
    Returns:
        dict: 职位等级列表
    """
    url = f"{base_url}/level/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "positionLevelStatus": positionLevelStatus,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def position_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    positionStatus: Optional[int] = None,
    basicDate: Optional[str] = None,) -> dict:
    """

    职位列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - 支持名称,编码
        positionStatus (int, None): 是否启用. Defaults to None.
            - 0: 禁用 1: 启用
        basicDate (str, None): 基准日起. Defaults to None.
            - 格式: YYYY-MM-DD
    Returns:
        dict: 职位列表
    """
    url = f"{base_url}/position/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "positionStatus": positionStatus,
        "basicDate": basicDate if basicDate else get_current_date(),
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def position_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    basicDate: Optional[str] = None,)->dict:
    """
    职位列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.

    Returns:
        dict: 职位列表
    """
    url = f"{base_url}/position/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "basicDate": basicDate if basicDate else get_current_date(),
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_b8f5e376-4900-4a32-87d4-d4fc959947f1"
    tenant_id = 148

    async def main():
        data = await position_list(authorization, tenant_id)
        print(data)

    asyncio.run(main())
