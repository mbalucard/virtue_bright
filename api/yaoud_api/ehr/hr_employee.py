"""
人员管理
    - 人员列表: employee_list
    - 人员列表字段配置: employee_list_settings_fields
    - 人员花名册字段配置: employee_roster_field_setting
    - 人员搜索条件字段配置: employee_search_condition_fields
    - 人员名册: employee_page_list
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

async def employee_list_settings_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    人员列表字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员列表字段配置
    """
    url = f"{base_url}/listSettingsFields"
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

async def employee_roster_field_setting(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    人员花名册字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员花名册字段配置
    """
    url = f"{base_url}/rosterFieldSetting"
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


async def employee_search_condition_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    人员搜索条件字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员搜索条件字段配置
    """
    url = f"{base_url}/searchConditionFields"
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



async def employee_page_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    conditions: Optional[List[dict]] = None,)->dict:
    """
    人员名册
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        conditions (List[dict], None): 检索条件. Defaults to None.
            - 可在 employee_search_condition_fields 中获取人员检索信息
            - 可在 position_list 中获取职位检索信息
            - 样例: [{"field":"basicDate","title":"基准日期","rule":"eq","ruleName":"等于","value":"2026-03-31","labelValue":"","valueType":8}]
    Returns:
        dict: 人员名册
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "conditions": conditions,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def employee_detail_work_info(
    authorization: str,
    id: int,
    version_id: int,
    tenant_id: Optional[int] = None,)->dict:
    """
    人员工作信息
    Args:
        authorization (str): 认证信息
        id (int): 人员ID.
            - 可在 employee_page_list 中获取  对应字段 id
        version_id (int): 版本ID.
            - 可在 employee_page_list 中获取  对应字段 versionId
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 人员工作信息
    """
    url = f"{base_url}/detail/workInfo/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "versionId": version_id,
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()




if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_b8f5e376-4900-4a32-87d4-d4fc959947f1"
    tenant_id = 148
    async def main():
        data = await employee_detail_work_info(
            authorization,
            id=707,
            version_id=821,
            tenant_id=tenant_id)
        print(data)
    asyncio.run(main())