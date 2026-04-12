"""
绩效管理
    - 绩效目标-目标列表: plan_h_list
    - 绩效目标-详情列名: plan_h_achieved_column
    - 绩效目标-目标详情列表: plan_h_achieved_target_list
    - 绩效目标-自动经营策略列表: plan_h_auto_manage_strategy_list
    - 提成方案-下拉检索用: commission_external_org_auth_filter_page
    - 提成方案-列表: commission_config_page
    - 手动计算任务列表: hand_do_work_list
    - 计算日志-目标激励: plan_motivation_conpute_log
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
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
        belongOrgIds: Optional[List[str]] = None,) -> dict:
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
        tenant_id: Optional[int] = None,) -> dict:
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
        size: int = 10,) -> dict:
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
        updateDateEnd: Optional[str] = None,) -> dict:
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


async def commission_external_org_auth_filter_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        keyword: Optional[str] = None,) -> dict:
    """
    提成方案-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键词. Defaults to None.
            - 支持检索提成方案名称 提成方案编码
    Returns:
        dict: 提成方案-下拉检索用
    """
    url = f"{base_url}/commission/external/orgAuthFilterPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "i18nCode": "ehr.router.commission.sales.details",
        "permission": None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def commission_config_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        onlyShowNoAuth: bool = False,
        permission: Optional[str] = None,
        ids: Optional[List[str]] = None,
        commissionPlanType: Optional[str] = "0",
        commissionStatus: Optional[str] = None,
        applyStoreArray: Optional[List[str]] = None,
        applyGoodsArray: Optional[List[str]] = None,
        belongOrgIds: Optional[List[str]] = None,
        commissionStartDate: Optional[str] = None,
        commissionEndDate: Optional[str] = None,) -> dict:
    """
    提成方案-列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        onlyShowNoAuth (bool): 是否仅显示不受组织权限控制的数据. Defaults to False.
        permission (str, None): 未知参数. Defaults to None.
        ids (List[str], None): 提成方案ID. Defaults to None.
            - 可在 commission_external_org_auth_filter_page 中获取
        commissionPlanType (str, None): 提成方案类型. Defaults to None.
            - 0:全部 10:基础提成 20:单品提成 30:组合提成 40:系列提成
        commissionStatus (str, None): 提成方案状态. Defaults to None.
            - 2:已生效 3:已停用 4:已过期 1:草稿
        applyStoreArray (List[str], None): 适用门店. Defaults to None.
            - 可在 get_mi_page 中获取 对应字段 id
        applyGoodsArray (List[str], None): 适用商品. Defaults to None.
            - 可在 external_goods_page_list 中获取 对应字段 ID需拼接"-3"
            - 样例: ["8462424206355924597-3"]
        belongOrgIds (List[str], None): 归属组织. Defaults to None.
            - 可在 auth_department_tree 中获取 对应字段 id
        commissionStartDate (str, None): 提成生效日期. Defaults to None.
            - 格式:yyyy-MM-dd
        commissionEndDate (str, None): 提成失效日期. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 提成方案-列表
    """
    url = f"{base_url}/commission/config/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "i18nCode": "ehr.router.commission.sales.details",
        "current": current,
        "size": size,
        "onlyShowNoAuth": onlyShowNoAuth,
        "permission": permission,
        "ids": ids,
        "commissionPlanType": commissionPlanType,
        "commissionStatus": commissionStatus,
        "applyStoreArray": applyStoreArray,
        "applyGoodsArray": applyGoodsArray,
        "belongOrgIds": belongOrgIds,
        "commissionStartDate": commissionStartDate,
        "commissionEndDate": commissionEndDate,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def hand_do_work_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    keyword: Optional[str] = None,)->dict:
    """
    手动计算任务列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        keyword (str, None): 关键字. Defaults to None.
            - #! 不知道能检索什么，反正不能检索计划ID
    Returns:
        dict: 手动计算任务列表
    """
    url = f"{base_url}/commission/planMotivationConputeLog/handDoWorkList"
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
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def plan_motivation_conpute_log(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    calcStatus: Optional[str] = None,
    calcType: Optional[str] = None,
    recalcTaskIds: Optional[List[str]] = None,
    planName: Optional[str] = None,
    calcDateBegin: Optional[str] = None,
    calcDateEnd: Optional[str] = None, )->dict:
    """
    计算日志-目标激励
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        calcStatus (str, None): 计算状态. Defaults to None.
            - 1:计算成功 2:计算失败
        calcType (str, None): 计算类型. Defaults to None.
            - 1:手动计算 2:自动计算
        recalcTaskIds (List[str], None): 手动计算任务ID. Defaults to None.
            - 可在 hand_do_work_list 中获取 对应字段planId
            - #! 这个字段受手动计算任务，但当该字段有值，calcType=1时，该字段无数据，carcType=2却有数据，到底是自动还是手动，逻辑混乱，小学语文都没毕业吧。垃圾
        planName (str, None): 计划名称. Defaults to None.
            - 计划名称  type:str
        calcDateBegin (str, None): 计算时间区间-开始. Defaults to None.
            - 格式:yyyy-MM-dd
        calcDateEnd (str, None): 计算时间区间-结束. Defaults to None.
            - 格式:yyyy-MM-dd
    Returns:
        dict: 计算日志-目标激励
    """
    url = f"{base_url}/planMotivationConputeLogD/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "i18nCode": "ehr.router.commission.sales.details",
        "current": current,
        "size": size,
        "calcStatus": calcStatus,
        "calcType": calcType,
        "planName": planName,
        "recalcTaskIds": recalcTaskIds,
        "calcDateBegin": calcDateBegin,
        "calcDateEnd": calcDateEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()



if __name__ == "__main__":
    import asyncio

    authorization = "Bearer new_c05d11d5-ceaf-4913-8ee7-0a3335205e83"
    tenant_id = 148

    async def main():
        data = await plan_motivation_conpute_log(
            authorization=authorization,
            tenant_id=tenant_id
        )
        print(data)
    asyncio.run(main())
