"""
申报管理
    - 员工信息申报管理搜索条件字段配置: manager_search_condition_fields
    - 员工信息申报管理列表: manager_page_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/self"
TTL = yaoud_env["timeout"]

async def manager_search_condition_fields(
    authorization: str,
    tenant_id: Optional[int] = None,)->dict:
    """
    员工信息申报管理搜索条件字段配置
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 搜索条件字段配置
    """

    url = f"{base_url}/manager/searchConditionFields"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_t":timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()

async def manager_page_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    name: Optional[str] = None,
    workNo: Optional[str] = None,
    applyStatus: Optional[List[int]] = None,
    employeeStatus: Optional[List[str]] = None,
    positiveStatus: Optional[List[str]] = None,
    jobType: Optional[List[str]] = None,
    organization: Optional[List[str]] = None,
    position: Optional[List[str]] = None,
    directLeader: Optional[List[str]] = None,
    workPlace: Optional[List[List[str]]] = None,
    submitDateStart: Optional[str] = None,
    submitDateEnd: Optional[str] = None,
    entryDateStart: Optional[str] = None,
    entryDateEnd: Optional[str] = None,) ->dict:
    """
    员工信息申报管理列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        name (str, None): 姓名. Defaults to None.
        workNo (str, None): 工号. Defaults to None.
        applyStatus (List[int], None): 申报状态. Defaults to None.
            - 10:审核中 20:已撤回 30:已驳回 40:已通过
        employeeStatus (List[str], None): 员工状态. Defaults to None.
            - 可在 manager_search_condition_fields 中获取
        positiveStatus (List[str], None): 转正状态. Defaults to None.
            - 可在 manager_search_condition_fields 中获取
        jobType (List[str], None): 在职类型. Defaults to None.
            - 可在 all_dict_items 中获取 字典编号: D802-002
        organization (List[str], None): 组织架构. Defaults to None.
            - 可在 department_tree 中获取 对应字段 mainTableId
        position (List[str], None): 职位. Defaults to None.
            - 可在 position_list 中获取 对应字段 id
        directLeader (List[str], None): 直属上级. Defaults to None.
            - 可在 employee_list 中获取 对应字段 id
        workPlace (List[List[str]], None): 工作地点. Defaults to None.
            - 可在 region_tree 中获取 格式: ["省ID", "市ID", "区ID"]
        submitDateStart (str, None): 提交日期区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        submitDateEnd (str, None): 提交日期区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        entryDateStart (str, None): 入职日期区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        entryDateEnd (str, None): 入职日期区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd   
    Returns:
        dict: 员工信息申报管理列表
    """
    url = f"{base_url}/manager/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "name": name,
        "workNo": workNo,
        "applyStatus": applyStatus,
        "employeeStatus": employeeStatus,
        "positiveStatus": positiveStatus,
        "jobType": jobType,
        "organization": organization,
        "position": position,
        "directLeader": directLeader,
        "workPlace": workPlace,
        "submitDateStart": submitDateStart,
        "submitDateEnd": submitDateEnd if submitDateEnd else get_current_date(),
        "entryDate":[entryDateStart, entryDateEnd if entryDateEnd else get_current_date()],
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()

if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_a05755b9-5b4b-40f6-bd0f-f34a0ebeb928"
    tenant_id = 148
    
    async def main():
        data = await manager_page_list(authorization, tenant_id)
        print(data)
    asyncio.run(main())