"""
薪资参数
    - 薪资参数-列表: salary_param_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrSalaryParam"
TTL = yaoud_env["timeout"]


async def get_salary_param(
        authorization: str,
        tenant_id: Optional[int] = None,
        ) -> dict:
    """
    薪资参数-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 薪资参数-列表
    """
    url = f"{base_url}/getSalaryParam"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()

if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_e989f1a7-81ea-453e-b282-f0e79a3494af"
    tenant_id = 148

    async def main():
        data = await get_salary_param(authorization, tenant_id)
        print(data)
    asyncio.run(main())