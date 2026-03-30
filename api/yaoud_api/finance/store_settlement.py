"""
门店结算
    - 门店结算单列表: store_settlement_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/storeSettlement"


async def store_settlement_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    settleNo: Optional[str] = None,
    sourceNo: Optional[str] = None,
    businessNo: Optional[str] = None,
    storesIdList: Optional[List[str]] = None,
    warehouseIdList: Optional[List[str]] = None,
    createIds: Optional[List[str]] = None,
    updateIds: Optional[List[str]] = None,
    createStartTime: Optional[str] = None,
    createEndTime: Optional[str] = None,
    finishAuditTimeStart: Optional[str] = None,
    finishAuditTimeEnd: Optional[str] = None,
    updateStartTime: Optional[str] = None,
    updateEndTime: Optional[str] = None,)->dict:
    """
    门店结算单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        settleNo (str, None): 单据编号. Defaults to None.
        sourceNo (str, None): 出入库单号. Defaults to None.
        businessNo (str, None): 业务单号. Defaults to None.
        storesIdList (List[str], None): 门店ID列表. Defaults to None.
            - 可在 select_stores 中获取
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 synergys_warehouse_info 中获取
        createIds (List[str], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        updateIds (List[str], None): 修改人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        finishAuditTimeStart (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        finishAuditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        updateStartTime (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        updateEndTime (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    Returns:
        dict: 门店结算单列表
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createStartTime:
        createStartTime = get_date_start_and_end_time(createStartTime)
    else:
        taday = get_current_date()
        createStartTime = get_date_start_and_end_time(taday)
    if createEndTime:
        createEndTime = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        createEndTime = get_date_start_and_end_time(taday)
    if finishAuditTimeStart:
        finishAuditTimeStart = get_date_start_and_end_time(finishAuditTimeStart)
    if finishAuditTimeEnd:
        finishAuditTimeEnd = get_date_start_and_end_time(finishAuditTimeEnd)
    if updateStartTime:
        updateStartTime = get_date_start_and_end_time(updateStartTime)
    if updateEndTime:
        updateEndTime = get_date_start_and_end_time(updateEndTime)
    payload = {
        "current": current,
        "size": size,
        "settleNo": settleNo,
        "sourceNo": sourceNo,
        "businessNo": businessNo,
        "storesIdList": storesIdList,
        "warehouseIdList": warehouseIdList,
        "createIds": createIds,
        "updateIds": updateIds,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "finishAuditTimeStart": finishAuditTimeStart['start_time'] if finishAuditTimeStart else None,
        "finishAuditTimeEnd": finishAuditTimeEnd['end_time'] if finishAuditTimeEnd else None,
        "updateStartTime": updateStartTime['start_time'] if updateStartTime else None,
        "updateEndTime": updateEndTime['end_time'] if updateEndTime else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
