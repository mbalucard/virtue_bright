"""
字段设置
    - 获取人事字段设置列表: get_field_setting_list
    - 获取人事字段设置详情: field_setting_detail
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrFieldSetting"


async def get_field_setting_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        isEnabled: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    获取人事字段设置列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        isEnabled (int, None): 是否启用. Defaults to None.
            - 0: 禁用 1: 启用
        keyword (str, None): 关键字. Defaults to None.
            - 支持名称,fieldCode
    Returns:
        dict: 字段设置列表
    """
    url = f"{base_url}/getFieldSettingList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "isEnabled": isEnabled,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def field_setting_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    获取人事字段设置详情
    Args:
        authorization (str): 认证信息
        id (int): 字段设置ID.
            - 可在 get_field_setting_list 中获取, 对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 字段设置详情
    """
    url = f"{base_url}/detail/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_b8f5e376-4900-4a32-87d4-d4fc959947f1"
    tenant_id = 148
    id = 415

    async def main():
        data = await field_setting_detail(authorization, id, tenant_id)
        print(data)

    asyncio.run(main())
