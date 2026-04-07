"""
绩效管理
    - 绩效目标-目标列表: plan_h_list
    - 绩效目标-详情列名: plan_h_achieved_column
    - 绩效目标-目标详情列表: plan_h_achieved_target_list
    - 绩效目标-自动经营策略列表: plan_h_auto_manage_strategy_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/commission"

async def plan_h_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    title: Optional[str] = None,
    onlyShowNoAuth: bool = False,
    permission: Optional[str] = None,
    status: Optional[int] = None,
    planSource: Optional[List[int]] = None,
    belongOrgIds: Optional[List[str]] = None,)->dict:
    """
    绩效目标-目标列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        title (str, None): 计划标题. Defaults to None.
        onlyShowNoAuth (bool): 是否仅显示不受组织权限控制的数据. Defaults to False.
        permission (str, None): 未知参数. Defaults to None.
        status (int, None): 状态. Defaults to None.
            - 1:启用 2:停用
        planSource (List[int], None): 计划创建方式. Defaults to None.
            - 1:系统创建 0:手动创建
        belongOrgIds (List[str], None): 归属组织. Defaults to None.
            - 可在 auth_department_tree 中获取
        #! 此处缺少一个参数，策略名称，等有数据了再确认
    Returns:
        dict: 绩效目标-目标列表
    """
    url = f"{base_url}/planH/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "i18nCode": "ehr.router.commission.target.plan.details",
        "current": current,
        "size": size,
        "title": title,
        "onlyShowNoAuth": onlyShowNoAuth,
        "permission": permission,
        "status": status,
        "planSource": planSource,
        "belongOrgIds": belongOrgIds,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def plan_h_achieved_column(
    authorization: str,
    id: int,
    tenant_id: Optional[int] = None,)->dict:
    """
    绩效目标-详情列名
    Args:
        authorization (str): 认证信息
        id (int): 绩效目标ID.
            - 可在 plan_h_list 中获取  对应字段 id
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 绩效目标-详情列名
    """
    url = f"{base_url}/planH/getAchievedColumn"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def plan_h_achieved_target_list(
    authorization: str,
    id: int,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,)->dict:
    """
    绩效目标-目标详情列表
    """
    url = f"{base_url}/planH/achievedTargetPageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "id": id,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def plan_h_auto_manage_strategy_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    strategyName: Optional[str] = None,
    updateUser: Optional[str] = None,
    onlyShowNoAuth: bool = False,
    permission: Optional[str] = None,
    strategyStatusList: Optional[List[int]] = None,
    enabledList: Optional[List[int]] = None,
    belongOrgIds: Optional[List[str]] = None,
    effectiveDateBegin: Optional[str] = None,
    effectiveDateEnd: Optional[str] = None,
    updateDateStart: Optional[str] = None,
    updateDateEnd: Optional[str] = None,)->dict:
    """
    绩效目标-自动经营策略列表
    #! 无数据，待确认
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        strategyName (str, None): 策略名称. Defaults to None.
        updateUser (str, None): 更新人. Defaults to None.
        onlyShowNoAuth (bool): 是否仅显示不受组织权限控制的数据. Defaults to False.
        permission (str, None): 未知参数. Defaults to None.
        strategyStatusList (List[int], None): 策略状态. Defaults to None.
            - 1:未开始 2:进行中 3:已过期
        enabledList (List[int], None): 启用状态. Defaults to None.
            - 1:已启用 0:未启用
        belongOrgIds (List[str], None): 归属组织. Defaults to None.
            - 可在 auth_department_tree 中获取
        effectiveDateBegin (str, None): 生效时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        effectiveDateEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
        updateDateStart (str, None): 更新时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        updateDateEnd (str, None): 更新时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 绩效目标-自动经营策略列表
    """
    url = f"{base_url}/planAutoManageStrategy/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "i18nCode": "ehr.router.commission.target.plan.details",
        "strategyName": strategyName,
        "updateUser": updateUser,
        "onlyShowNoAuth": onlyShowNoAuth,
        "permission": permission,
        "strategyStatusList": strategyStatusList,
        "enabledList": enabledList,
        "belongOrgIds": belongOrgIds,
        "effectiveDateBegin": effectiveDateBegin,
        "effectiveDateEnd": effectiveDateEnd,
        "updateDateStart": updateDateStart,
        "updateDateEnd": updateDateEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_3f765ea0-fd65-43e8-9d18-f9b5f5151f9a"
    tenant_id = 148

    async def main():
        data = await plan_h_auto_manage_strategy_list(
            authorization=authorization, 
            tenant_id=tenant_id
            )
        print(data)
    asyncio.run(main())