"""
损益管理
    - 报损报溢-按单据: loss_overflow_page
    - 报损报溢-按商品: loss_overflow_detail
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/inventory/loss"
TTL = yaoud_env["timeout"]


async def loss_overflow_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        documentNo: Optional[str] = None,
        businessNo: Optional[str] = None,
        createName: Optional[str] = None,
        submitName: Optional[str] = None,
        businessTypeList: Optional[List[str]] = None,
        status: Optional[str] = None,
        warehouseIds: Optional[List[str]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        submitTimeBegin: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    报损报溢-按单据
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNo (str, None): 单据号. Defaults to None.
        businessNo (str, None): 业务单号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        submitName (str, None): 提交人. Defaults to None.
        businessTypeList (List[str], None): 业务类型. Defaults to None.
            - 可选值：CLEAR_LOSS-损溢清斗单 APPLY_LOSS-损溢申请单 HAND_OVERFLOW-手动创建损溢单 HAND_DISMANTLE-拆零
        status (str, None): 单据状态. Defaults to None.
            - 可选值：DRAFT-草稿 SUBMITTED-审批中 COMPLETED-已完成 CANCEL-已作废 CLOSED-已关闭 TURN-已驳回
        warehouseIds (List[str], None): 仓库ID. Defaults to None.
            - 可在 ent_store_warehouse_query 中获取，对应字段id
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeBegin (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}/overflow/apply/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createTimeBegin:
        create_time_begin = get_date_start_and_end_time(createTimeBegin)
    else:
        taday = get_current_date()
        create_time_begin = get_date_start_and_end_time(taday)
    if createTimeEnd:
        create_time_end = get_date_start_and_end_time(createTimeEnd)
    else:
        create_time_end = None

    if submitTimeBegin:
        submitTimeBegin = get_date_start_and_end_time(submitTimeBegin)
    if submitTimeEnd:
        submitTimeEnd = get_date_start_and_end_time(submitTimeEnd)
    if takeEffectTimeStart:
        takeEffectTimeStart = get_date_start_and_end_time(takeEffectTimeStart)
    if takeEffectTimeEnd:
        takeEffectTimeEnd = get_date_start_and_end_time(takeEffectTimeEnd)
    payload = {
        "current": current,
        "size": size,
        "apply": 0,
        "type": 3,
        "documentNo": documentNo,
        "businessNo": businessNo,
        "createName": createName,
        "submitName": submitName,
        "businessTypeList": businessTypeList,
        "status": status,
        "warehouseIds": warehouseIds,
        "createTimeBegin": create_time_begin['start_time'] if create_time_begin else None,
        "createTimeEnd": create_time_end['end_time'] if create_time_end else None,
        "submitTimeBegin": submitTimeBegin['start_time'] if submitTimeBegin else None,
        "submitTimeEnd": submitTimeEnd['end_time'] if submitTimeEnd else None,
        "takeEffectTimeStart": takeEffectTimeStart['start_time'] if takeEffectTimeStart else None,
        "takeEffectTimeEnd": takeEffectTimeEnd['end_time'] if takeEffectTimeEnd else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def loss_overflow_detail(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        documentNo: Optional[str] = None,
        keyword: Optional[str] = None,
        batch: Optional[str] = None,
        reason: Optional[str] = None,
        createName: Optional[str] = None,
        submitName: Optional[str] = None,
        status: Optional[str] = None,
        lossOrOverflow: Optional[str] = None,
        businessTypeList: Optional[List[str]] = None,
        warehouseIds: Optional[List[str]] = None,
        regionIds: Optional[List[str]] = None,
        purchaserIds: Optional[List[str]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        submitTimeBegin: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    报损报溢-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNo (str, None): 单据号. Defaults to None.
        keyword (str, None): 商品关键字检索. Defaults to None.
            - 支持通用名称，商品名称，商品助记码，通用名称助记码，批准文号，生产企业
        batch (str, None): 批次号. Defaults to None.
        reason (str, None): 损溢原因. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        submitName (str, None): 提交人. Defaults to None.
        status (str, None): 单据状态. Defaults to None.
            - 可选值：DRAFT-草稿 SUBMITTED-审批中 COMPLETED-已完成 CANCEL-已作废 CLOSED-已关闭 TURN-已驳回
        lossOrOverflow (str, None): 损溢类型. Defaults to None.
            - 可选值：loss-损单 overflow-溢单
        businessTypeList (List[str], None): 业务类型. Defaults to None.
            - 可选值：CLEAR_LOSS-损溢清斗单 APPLY_LOSS-损溢申请单 HAND_OVERFLOW-手动创建损溢单 HAND_DISMANTLE-拆零
        warehouseIds (List[str], None): 仓库ID. Defaults to None.
            - 可在 ent_store_warehouse_query 中获取，对应字段id
        regionIds (List[str], None): 区域ID. Defaults to None.
            - 可在 ent_store_warehouse_query 中获取，对应字段id
        purchaserIds (List[str], None): 采购员ID. Defaults to None.
            - 可在 get_employee_list 中获取 postCodes:POST_BUYER
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeBegin (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}/overflow/apply/detailPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createTimeBegin:
        create_time_begin = get_date_start_and_end_time(createTimeBegin)
    else:
        taday = get_current_date()
        create_time_begin = get_date_start_and_end_time(taday)
    if createTimeEnd:
        create_time_end = get_date_start_and_end_time(createTimeEnd)
    else:
        create_time_end = None
    if submitTimeBegin:
        submitTimeBegin = get_date_start_and_end_time(submitTimeBegin)
    if submitTimeEnd:
        submitTimeEnd = get_date_start_and_end_time(submitTimeEnd)
    if takeEffectTimeStart:
        takeEffectTimeStart = get_date_start_and_end_time(takeEffectTimeStart)
    if takeEffectTimeEnd:
        takeEffectTimeEnd = get_date_start_and_end_time(takeEffectTimeEnd)
    payload = {
        "current": current,
        "size": size,
        "type": 3,
        "apply": 0,
        "documentNo": documentNo,
        "keyword": keyword,
        "batch": batch,
        "reason": reason,
        "createName": createName,
        "submitName": submitName,
        "status": status,
        "lossOrOverflow": lossOrOverflow,
        "businessTypeList": businessTypeList,
        "warehouseIds": warehouseIds,
        "regionIds": regionIds,
        "purchaserIds": purchaserIds,
        "createTimeBegin": create_time_begin['start_time'] if create_time_begin else None,
        "createTimeEnd": create_time_end['end_time'] if create_time_end else None,
        "submitTimeBegin": submitTimeBegin['start_time'] if submitTimeBegin else None,
        "submitTimeEnd": submitTimeEnd['end_time'] if submitTimeEnd else None,
        "takeEffectTimeStart": takeEffectTimeStart['start_time'] if takeEffectTimeStart else None,
        "takeEffectTimeEnd": takeEffectTimeEnd['end_time'] if takeEffectTimeEnd else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
