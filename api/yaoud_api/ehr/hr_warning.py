"""
预警
    - 预警检索字段: profession_warn_search_condition_fields
    - 预警字段配置: profession_warn_settings_fields
    - 专业证照预警: profession_warn_page
    - 合同预警字段配置: contract_warn_settings_fields
    - 合同预警字段搜索: contract_warn_search_condition_fields
    - 员工合同预警: contract_warn_page
    - 员工质量岗位变动-检索条件: qa_post_employee_change_search_condition_fields
    - 员工质量岗位变动: quality_post_employee_change_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrWarning"


async def profession_warn_search_condition_fields(
    authorization: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    预警检索字段
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 预警检索字段
    """
    url = f"{base_url}/profession/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()



async def profession_warn_settings_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    预警字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 预警字段配置
    """
    url = f"{base_url}/profession/listSettingsFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t":timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def profession_warn_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    conditions: Optional[List[dict]] = None,)->dict:
    """
    专业证照预警
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        conditions (List[dict], None): 检索条件. Defaults to None.
            - 可在 profession_warn_search_condition_fields 中获取预警检索信息
            - 样例: [{"field":"name","rule":"like","value":"张三"}]
            - field: 对应field字段 rule: 对应expression字段 
            - value: 
                - valueType 为0 tyep:str, 
                - valueType 为1 type:list[str | int] 选项对应fixSelectValue字段中的 code, 
                - valueType 为2 tyep:list[str] 格式为[yyyy-MM-dd,yyyy-MM-dd], 意思为时间区间
    Returns:
        dict: 专业证照预警
    """
    url = f"{base_url}/pageProfessionWarn"
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
    

async def contract_warn_settings_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    合同预警字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 合同预警字段配置
    """
    url = f"{base_url}/contract/listSettingsFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t":timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def contract_warn_search_condition_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    合同预警字段搜索
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 合同预警字段搜索
    """
    url = f"{base_url}/contract/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t":timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def contract_warn_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    conditions: Optional[List[dict]] = None,)->dict:
    """
    员工合同预警
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        conditions (List[dict], None): 检索条件. Defaults to None.
            - 可在 contract_warn_search_condition_fields 中获取预警检索信息
            - 样例: [{"field":"name","rule":"like","value":"张三"}]
            - field: 对应field字段 rule: 对应expression字段 
            - value: 
                - valueType 为0 tyep:str, 
                - valueType 为1 type:list[str | int] 选项对应fixSelectValue字段中的 code, 若fixSelectValue字段为空, 则在filterApi对应的API中获取选项
                - valueType 为2 tyep:list[str] 格式为[yyyy-MM-dd,yyyy-MM-dd], 意思为时间区间
                - valueType 为6 type:list[int] 格式为[1,2] 意思为数据范围区间
    Returns:
        dict: 员工合同预警
    """
    url = f"{base_url}/pageContractWarn"
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


async def qa_post_employee_change_search_condition_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    员工质量岗位变动-检索条件
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 员工质量岗位变动-检索条件
    """
    url = f"{base_url}/qaPostEmployeeChange/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t":timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def quality_post_employee_change_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    conditions: Optional[List[dict]] = None,)->dict:
    """
    员工质量岗位变动
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        conditions (List[dict], None): 检索条件. Defaults to None.
            - 可在 qa_post_employee_change_search_condition_fields 中获取预警检索信息
            - 样例: [{"field":"name","rule":"like","value":"张三"}]
            - field: 对应field字段 rule: 对应expression字段 
            - value: 
                - valueType 为0 tyep:str, 
                - valueType 为1 type:list[str | int] 选项对应fixSelectValue字段中的 code, 若fixSelectValue字段为空, 则在filterApi对应的API中获取选项
                - valueType 为2 tyep:list[str] 格式为[yyyy-MM-dd,yyyy-MM-dd], 意思为时间区间
                - valueType 为6 type:list[int] 格式为[1,2] 意思为数据范围区间
                - dictCode 不为空，可在 all_dict_items 中获取选项
    """
    url = f"{base_url}/getQualityPostEmployeeChangePage"
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

if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_521d29cf-d5dd-450c-b2d0-9c05ebe77c50"
    tenant_id = 148

    async def main():
        data = await qa_post_employee_change_search_condition_fields(
            authorization,
            tenant_id)
        print(data)
    asyncio.run(main())
