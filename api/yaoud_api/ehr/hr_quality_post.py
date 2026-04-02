"""
岗位
    - 质量岗位列表: quality_post_page
    - 质量岗位列表: quality_post_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrQualityPost"

async def quality_post_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,
    enable: Optional[int] = None,
    erpPostCodes: Optional[List[str]] = None,
    professionTypes: Optional[List[str]] = None,)->dict:
    """
    质量岗位列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - 支持名称
        enable (int, None): 是否启用. Defaults to None.
            - 0: 禁用 1: 启用
        erpPostCodes (List[str], None): erp职位编码. Defaults to None.
            - 可在 all_dict_items 中获取
        professionTypes (List[str], None): 证照类型. Defaults to None.
            - 可在 all_dict_items 中获取
    Returns:
        dict: 质量岗位列表
    """
    url = f"{base_url}/queryPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "enable": enable,
        "erpPostCodes": erpPostCodes,
        "professionTypes": professionTypes,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def quality_post_list(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    质量岗位列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 质量岗位列表
    """
    url = f"{base_url}/queryList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t":timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_d5e00235-3fd3-442f-9526-ab312d40d115"
    tenant_id = 148

    async def main():
        data = await quality_post_list(authorization, tenant_id)
        print(data)

    asyncio.run(main())