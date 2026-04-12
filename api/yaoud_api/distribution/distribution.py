"""
铺货
    - 铺货单-单据详情: distribution_docs_detail
    - 铺货计划列表: distribution_plan_list
    - 铺货单-按明细: distribution_goods_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/distribution/distribution"
TTL = yaoud_env["timeout"]

async def distribution_docs_detail(
        authorization: str,
        document_id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    铺货单-单据详情
    Args:
        authorization (str): 认证信息
        document_id (str): 铺货单ID
        tenant_id (int, None): 租户ID. Defaults to None.
    """
    url = f"{base_url}/info/{document_id}"
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


async def distribution_plan_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        whether_details: bool = False,
        current: int = 1,
        size: int = 10,
        status: Optional[str] = None,
        goodsCodes: Optional[List[str]] = None,
        storeIds: Optional[List[str]] = None,
        orderNo: Optional[str] = None,
        startDate: Optional[str] = None,
        endDate: Optional[str] = None,) -> dict:
    """
    铺货计划列表
    #! 无数据，暂未验证
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        whether_details (bool): 是否包含详情. Defaults to False.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        status (str, None): 单据状态. Defaults to None.
            - 1-首营中,3-已完成,4-已作废,5-已关闭,6-待调用,7-调用中,8-已过期,None-全部
        goodsCodes (List[str], None): 商品编码列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        storeIds (List[str], None): 门店ID列表. Defaults to None.
            - 可在 select_stores 中获取
        orderNo (str, None): 单据编号. Defaults to None.
        startDate (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        endDate (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 铺货计划列表
    """
    if whether_details:
        url = f"{base_url}Plan/pageDetail"
    else:
        url = f"{base_url}Plan/page"

    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    # 时间格式转化，输出为YYYY-MM-DD HH:mm:ss
    if startDate:
        start_date = get_date_start_and_end_time(startDate)
    else:
        taday = get_current_date()
        start_date = get_date_start_and_end_time(taday)
    if endDate:
        end_date = get_date_start_and_end_time(endDate)
    else:
        end_date = None

    payload = {
        "current": current,
        "size": size,
        "status": status,
        "goodsCodes": goodsCodes,
        "storeIds": storeIds,
        "orderNo": orderNo,
        "startDate": start_date['start_time'] if start_date else None,
        "endDate": end_date['end_time'] if end_date else None,
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def distribution_goods_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        documentNo: Optional[str] = None,
        warehouseId: Optional[str] = None,
        storeId: Optional[str] = None,
        createName: Optional[str] = None,
        status: Optional[str] = None,
        goodsIds: Optional[List[str]] = None,
        batch: Optional[str] = None,
        batchNo: Optional[str] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        submitTimeBegin: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,
        takeEffectTimeBegin: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    铺货单-按明细
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        documentNo (str, None): 铺货单号. Defaults to None.
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取
        storeId (str, None): 门店ID. Defaults to None.
            - 可在 select_stores 中获取
        createName (str, None): 制单人姓名. Defaults to None.
        status (str, None): 单据状态. Defaults to None.
            - DRAFT:草稿,SUBMITTED:审批中，WAIT_APPROVAL：待批准，COMPLETED：已完成，CLOSED：已关闭，CANCEL：已作废
        goodsIds (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        batch (str, None): 批次号. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeBegin (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeBegin (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}Dtl/pageDetail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    # 时间格式转化，输出为YYYY-MM-DD HH:mm:ss
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
        submit_time_begin = get_date_start_and_end_time(submitTimeBegin)
    else:
        submit_time_begin = None
    if submitTimeEnd:
        submit_time_end = get_date_start_and_end_time(submitTimeEnd)
    else:
        submit_time_end = None
    payload = {
        "apply": 1,
        "type": 3,
        "current": current,
        "size": size,
        "documentNo": documentNo,
        "warehouseId": warehouseId,
        "storeId": storeId,
        "createName": createName,
        "status": status,
        "goodsIds": goodsIds,
        "batch": batch,
        "batchNo": batchNo,
        "createTimeBegin": create_time_begin['start_time'] if create_time_begin else None,
        "createTimeEnd": create_time_end['end_time'] if create_time_end else None,
        "submitTimeBegin": submit_time_begin['start_time'] if submit_time_begin else None,
        "submitTimeEnd": submit_time_end['end_time'] if submit_time_end else None,
        "takeEffectTimeBegin": takeEffectTimeBegin,
        "takeEffectTimeEnd": takeEffectTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
