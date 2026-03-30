"""
组织架构
    - 组织架构树-下拉检索用: department_tree
    - 组织架构列表: hr_organization_page_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/ehr/hrOrganization"


async def department_tree(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    组织架构树-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 组织架构树
    """
    url = f"{base_url}/departmentTree"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {"_": timestamp()}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def hr_organization_page_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    status: int = 1,
    employeeIsCorporation: Optional[int] = None,
    baseDate: Optional[str] = None,
    departmentCode: Optional[str] = None,
    departmentTypeCode: Optional[str] = None,
    departmentHeadId: Optional[int] = None,
    superiorDepartmentCode: Optional[str] = None,
    clinicStoreCode: Optional[str] = None,
) -> dict:
    """
    组织架构列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        status (int): 状态. Defaults to 1.
            - 1-启用 0-停用
        employeeIsCorporation (int, None): 员工是否为公司. Defaults to None.
            - 1-是 0-否
        baseDate (str, None): 基础日期. Defaults to None.
            - 格式:yyyy-MM-dd
        departmentCode (str, None): 部门编码. Defaults to None.
            - 部门名称 部门编码
        departmentTypeCode (str, None): 部门类型编码. Defaults to None.
            - 可在 all_dict_items 中获取
        departmentHeadId (int, None): 部门负责人ID. Defaults to None.
            - 可在 employee_list 中获取
        superiorDepartmentCode (str, None): 上级部门编码. Defaults to None.
            - 可在 department_tree 中获取
        clinicStoreCode (str, None): 门店编码. Defaults to None.
            - 可在 get_mi_page 中获取 对应字段 code
    Returns:
        dict: 组织架构列表
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    
    payload = {
        "status": status,
        "employeeIsCorporation": employeeIsCorporation,
        "baseDate": baseDate if baseDate else get_current_date(),
        "departmentCode": departmentCode,
        "departmentTypeCode": departmentTypeCode,
        "departmentHeadId": departmentHeadId,
        "superiorDepartmentCode": superiorDepartmentCode,
        "clinicStoreCode": clinicStoreCode,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_2523d693-9265-4016-a6e3-e34f5a5dff90"
    tenant_id = 148
    print(asyncio.run(hr_organization_page_list(authorization, tenant_id)))
