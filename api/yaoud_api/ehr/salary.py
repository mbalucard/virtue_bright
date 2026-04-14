"""
薪资管理
    - 社保公积金方案-列表: insurance_plan_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/salary"
TTL = yaoud_env["timeout"]


async def insurance_plan_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    keyword: Optional[str] = None,)->dict:
    """
    社保公积金方案-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        keyword (str, None): 关键字. Defaults to None.
            - 名称或编号
    Returns:
        dict: 社保公积金方案-列表
    """
    url = f"{base_url}/insurance/plan/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()

if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_e989f1a7-81ea-453e-b282-f0e79a3494af"
    tenant_id = 148

    async def main():
        data = await insurance_plan_page(authorization, tenant_id)
        print(data)
    asyncio.run(main())