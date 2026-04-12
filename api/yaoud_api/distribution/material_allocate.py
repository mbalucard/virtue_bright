"""
调拨
    - 调拨单列表: goods_transfer_list
    - 调拨单-按明细(含汇总): goods_transfer_detail_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/distribution/dsMaterialAllocate"


async def goods_transfer_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        billNo: Optional[str] = None,
        createName: Optional[str] = None,
        outStoCode: Optional[str] = None,
        inStoCode: Optional[str] = None,
        status: Optional[int] = None,
        createStartTime: str = get_current_date(),
        createEndTime: str = get_current_date(),
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        confirmTimeStart: Optional[str] = None,
        confirmTimeEnd: Optional[str] = None,) -> dict:
    """
    调拨单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        billNo (str, None): 单据号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        outStoCode (str, None): 出库门店编码. Defaults to None.
            - 可在 select_stores 中获取 对应字段 storeCode
        inStoCode (str, None): 入库门店编码. Defaults to None.
            - 可在 select_stores 中获取 对应字段 storeCode
        status (int, None): 单据状态. Defaults to None.
            - (0:草稿，1:审批中，6:待确认，2:处理中，3:已完成，4:已作废，7:已关闭，5:已驳回，8:确认失败)
        createStartTime (str): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createEndTime (str): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 有效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 有效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        confirmTimeStart (str, None): 确认时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        confirmTimeEnd (str, None): 确认时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 调拨单列表
    """
    url = f"{base_url}/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createStartTime:
        create_start_time = get_date_start_and_end_time(createStartTime)
        if create_start_time is None:
            raise ValueError("createStartTime 格式错误")
    else:
        taday = get_current_date()
        create_start_time = get_date_start_and_end_time(taday)
    if createEndTime:
        create_end_time = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        create_end_time = get_date_start_and_end_time(taday)
    payload = {
        "current": current,
        "size": size,
        "billType": 3,
        "billNo": billNo,
        "createName": createName,
        "outStoCode": outStoCode,
        "inStoCode": inStoCode,
        "status": status,
        "createStartTime": create_start_time['start_time'] if create_start_time else None,
        "createEndTime": create_end_time['end_time'] if create_end_time else None,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "confirmTimeStart": confirmTimeStart,
        "confirmTimeEnd": confirmTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()



async def goods_transfer_detail_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        billNo: Optional[str] = None,
        createName: Optional[str] = None,
        keyword: Optional[str] = None,
        proSpec: Optional[str] = None,
        barcode: Optional[str] = None,
        batchNo: Optional[str] = None,
        status: Optional[int] = None,
        outStoCode: Optional[str] = None,
        inStoCode: Optional[str] = None,
        code: Optional[str] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        expiryDateStart: Optional[str] = None,
        expiryDateEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        confirmTimeStart: Optional[str] = None,
        confirmTimeEnd: Optional[str] = None,) -> dict:
    """
    调拨单-按明细(含汇总)
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        billNo (str, None): 单据号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        keyword (str, None): 商品名称或编码. Defaults to None.
        proSpec (str, None): 商品规格. Defaults to None.
        barcode (str, None): 商品条码. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        status (int, None): 单据状态. Defaults to None.
            - (0:草稿，1:审批中，6:待确认，2:处理中，3:已完成，4:已作废，7:已关闭，5:已驳回，8:确认失败)
        outStoCode (str, None): 出库门店编码. Defaults to None.
            - 可在 select_stores 中获取 对应字段 storeCode
        inStoCode (str, None): 入库门店编码. Defaults to None.
            - 可在 select_stores 中获取 对应字段 storeCode
        code (str, None): 商品编码. Defaults to None.
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        expiryDateStart (str, None): 有效期区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        expiryDateEnd (str, None): 有效期区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 有效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 有效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        confirmTimeStart (str, None): 确认时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        confirmTimeEnd (str, None): 确认时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}D/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createStartTime:
        create_start_time = get_date_start_and_end_time(createStartTime)
        if create_start_time is None:
            raise ValueError("createStartTime 格式错误")
    else:
        taday = get_current_date()
        create_start_time = get_date_start_and_end_time(taday)
    if createEndTime:
        create_end_time = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        create_end_time = get_date_start_and_end_time(taday)
    params = {
        "current": current,
        "size": size,
        "billType": 3,
        "billNo": billNo,
        "createName": createName,
        "keyword": keyword,
        "proSpec": proSpec,
        "barcode": barcode,
        "batchNo": batchNo,
        "status": status,
        "outStoCode": outStoCode,
        "inStoCode": inStoCode,
        "code": code,
        "createStartTime": create_start_time['start_time'] if create_start_time else None,
        "createEndTime": create_end_time['end_time'] if create_end_time else None,
    }
    if expiryDateStart:
        params["expiryDateStart"] = expiryDateStart
    if expiryDateEnd:
        params["expiryDateEnd"] = expiryDateEnd
    if takeEffectTimeStart:
        params["takeEffectTimeStart"] = takeEffectTimeStart
    if takeEffectTimeEnd:
        params["takeEffectTimeEnd"] = takeEffectTimeEnd
    if confirmTimeStart:
        params["confirmTimeStart"] = confirmTimeStart
    if confirmTimeEnd:
        params["confirmTimeEnd"] = confirmTimeEnd
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
