"""
组织架构
    - 组织架构树-下拉检索用: department_tree
    - 组织架构列表: organization_page_list
    - 组织架构详情: organization_detail
    - 人事同步日志-组织: organization_sync_log
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


async def organization_page_list(
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


async def organization_detail(
    authorization: str,
    id: int,
    version_id: int,
    tenant_id: Optional[int] = None,)->dict:
    """
    组织架构详情
    Args:
        authorization (str): 认证信息
        id (int): 组织架构ID
            - 可在 organization_page_list 中获取  对应字段 id
        version_id (int): 版本ID
            - 可在 organization_page_list 中获取  对应字段 versionId
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 组织架构详情
    """
    url = f"{base_url}/detail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "versionId": version_id,
        "id": id,
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def organization_sync_log(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    syncDepartmentName: Optional[str] = None,
    calcStatus: Optional[str] = None,
    syncType: Optional[str] = None,
    syncDisType: Optional[int] = None,
    syncSystem: Optional[int] = None,
    syncTimeStart: Optional[str] = None,
    syncTimeEnd: Optional[str] = None,)->dict:
    """
    人事同步日志-组织
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        syncDepartmentName (str, None): 组织名称. Defaults to None.
        calcStatus (str, None): 状态. Defaults to None.
            - 0:失败 1:成功
        syncType (str, None): 同步类型. Defaults to None.
            - 1:新增 2:变更 3:删除
        syncDisType (int, None): 同步类别. Defaults to None.
            - 0:回传 1:推送
        syncSystem (int, None): 同步系统. Defaults to None.
            - 1:药德 2:企业微信 3:飞书
        syncTimeStart (str, None): 同步时间开始. Defaults to None.
            - 格式:yyyy-MM-dd
        syncTimeEnd (str, None): 同步时间结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 人事同步日志-组织
    """
    url = f"{base_url}EmployeeLog/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "syncDepartmentName": syncDepartmentName,
        "calcStatus": calcStatus,
        "syncType": syncType,
        "syncDisType": syncDisType,
        "syncSystem": syncSystem,
        "syncTimeStart": syncTimeStart if syncTimeStart else get_current_date(),
        "syncTimeEnd": syncTimeEnd if syncTimeEnd else get_current_date(),
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()




if __name__ == "__main__":
    import asyncio
    authorization = "Bearer new_521d29cf-d5dd-450c-b2d0-9c05ebe77c50"
    tenant_id = 148
    id = 4
    version_id = 4
    async def main():
        data = await organization_detail(
            authorization, 
            id=id,
            version_id=version_id, 
            tenant_id=tenant_id)
        print(data)
    asyncio.run(main())
