"""
薪资管理
    - 薪资参数-列表: salary_param_page
    - 薪资常量-列表: salary_const_page
    - 薪资项-列表: salary_item_page
    - 薪资项-详情: salary_item_detail
    - 算薪表模版-列表: salary_cal_template_page
    - 算薪表模版-详情: salary_cal_template_detail
    - 薪资档案设置字段: salary_archive_list_settings_fields
    - 薪资档案检索字段: salary_archive_search_condition_fields
    - 薪资档案-列表: salary_archive_page
    - 算薪表-列表: salary_cal_table_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrSalary"
TTL = yaoud_env["timeout"]


async def get_salary_param(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    薪资参数-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 薪资参数-列表
    """
    url = f"{base_url}Param/getSalaryParam"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def salary_const_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        enabled: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    薪资常量-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        enabled (int, None): 是否启用. Defaults to None.
            - 0:禁用 1:启用
        keyword (str, None): 关键字. Defaults to None.
            - 名称或编号
    """
    url = f"{base_url}Const/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "enabled": enabled,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def salary_const_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    薪资常量-详情
    Args:
        authorization (str): 认证信息
        id (int): 薪资常量ID.
            - 可在 salary_const_page 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 薪资常量-详情
    """
    url = f"{base_url}Const/detail/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def salary_item_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        enabled: Optional[int] = None,
        dataType: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    薪资项-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        enabled (int, None): 是否启用. Defaults to None.
            - 0:禁用 1:启用
        dataType (int, None): 数据类型. Defaults to None.
            - 1:录入项 2:销售提成 3:目标提成 4:公式项 5:系统项
        keyword (str, None): 关键字. Defaults to None.
            - 可检索名称或编号
    Returns:
        dict: 薪资项-列表
    """
    url = f"{base_url}/item/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "enabled": enabled,
        "dataType": dataType,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def salary_item_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    薪资项-详情
    Args:
        authorization (str): 认证信息
        id (int): 薪资项ID.
            - 可在 salary_item_page 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 薪资项-详情
    """
    url = f"{base_url}/item/detail/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def salary_cal_template_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,) -> dict:
    """
    算薪表模版-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        keyword (str, None): 关键字. Defaults to None.
            - 可检索名称或编号
    Returns:
        dict: 算薪表模版-列表
    """
    url = f"{base_url}CalTemplate/page"
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


async def salary_cal_template_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    算薪表模版-详情
    Args:
        authorization (str): 认证信息
        id (int): 算薪表模版ID.
            - 可在 salary_cal_template_page 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 算薪表模版-详情
    """
    url = f"{base_url}CalTemplate/detail/{id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def salary_archive_list_settings_fields(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    薪资档案设置字段
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 薪资档案设置字段
    """
    url = f"{base_url}Archive/listSettingsFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def salary_archive_search_condition_fields(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    薪资档案检索字段
    """
    url = f"{base_url}Archive/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def salary_archive_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        conditions: Optional[List[dict]] = None,) -> dict:
    """
    薪资档案-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        conditions (List[dict], None): 检索条件. Defaults to None.
            - 可在 salary_archive_search_condition_fields 中获取薪资档案检索信息
            - 样例: [{"field":"name","rule":"like","value":"张三"}]
            - field: 对应field字段 rule: 对应expression字段 
    """
    url = f"{base_url}Archive/pageList"
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
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_ea5e2854-a277-4c90-9eb1-6b9bb50a7a40"
    tenant_id = 148

    async def main():
        data = await salary_archive_page(
            authorization,
            tenant_id=tenant_id)
        print(data)
    asyncio.run(main())
