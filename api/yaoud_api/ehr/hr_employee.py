"""
人员管理
    - 人员列表: employee_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrEmployee"


async def employee_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    basicDate: str = get_current_date(),)->dict:
    """
    人员列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        basicDate (str): 基础日期. Defaults today .
            - 格式:yyyy-MM-dd
    Returns:
        dict: 人员列表
    """
    url = f"{base_url}/employee/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "basicDate": basicDate,
        "_": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_2523d693-9265-4016-a6e3-e34f5a5dff90"
    tenant_id = 148
    print(asyncio.run(employee_list(authorization, tenant_id)))