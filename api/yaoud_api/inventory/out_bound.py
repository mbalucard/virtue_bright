"""
出库管理
    - 出库-出库单-按单据: putbound_post_list
    - 出库-出库单-按商品: outbound_post_goods
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/inventory/outbound"
TTL = yaoud_env["timeout"]


async def putbound_post_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    sort: Optional[str] = None,
    sortField: Optional[str] = None,
    printed: Optional[int] = None,
    outboundNo: Optional[str] = None,
    businessNo: Optional[str] = None,
    toWarehouseName: Optional[str] = None,
    createId: Optional[str] = None,
    handledId: Optional[str] = None,
    submitId: Optional[str] = None,
    businessTypeList: Optional[List[int]] = None,
    businessSourceTypeList: Optional[List[int]] = None,
    warehouseIds: Optional[List[str]] = None,
    storeId: Optional[str] = None,
    # ? 这里少了一个客户ID字段，类型是List[str]，可在 external_member_list 中获取
    supplierIds: Optional[List[str]] = None,
    createTimeStart: Optional[str] = None,
    createTimeEnd: Optional[str] = None,
    submitTimeBegin: Optional[str] = None,
    submitTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
        total: bool = False,) -> dict:
    """
    出库-出库单-按单据
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        sort (str, None): 排序方式. Defaults to None.
            - asc-升序
            - desc-降序
        sortField (str, None): 排序字段. Defaults to None.
        printed (int, None): 是否打印. Defaults to None.
            - 1-是
            - 0-否
        outboundNo (str, None): 出库单号. Defaults to None.
        businessNo (str, None): 业务单号. Defaults to None.
        toWarehouseName (str, None): 接收仓库名称. Defaults to None.
            - 需全称
        createId (str, None): 制单人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        handledId (str, None): 处理人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        submitId (str, None): 提交人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        businessTypeList (List[int], None): 业务类型列表. Defaults to None.
            - 可在 out_bound_type 中获取，operateType=7
        businessSourceTypeList (List[int], None): 业务来源类型列表. Defaults to None.
        warehouseIds (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        storeId (str, None): 门店ID. Defaults to None.
            - 可在 select_store_warehouse 中获取
        supplierIds (List[str], None): 客户ID列表. Defaults to None.
            - 可在 external_member_list 中获取
        createTimeStart (str, None): 制单时间区间-开始. Defaults to None.
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
        total (bool, None): 是否查询总数. Defaults to False.
            - True: 查询总数
            - False: 查询分页数据
    Returns:
        dict: 出库-出库单-按单据响应体
    """
    if total:
        url = f"{base_url}/selectPostPageTotalSummary"
    else:
        url = f"{base_url}/selectPostPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "sort": sort,
        "sortField": sortField,
        "printed": printed,
        "outboundNo": outboundNo,
        "businessNo": businessNo,
        "toWarehouseName": toWarehouseName,
        "createId": createId,
        "handledId": handledId,
        "submitId": submitId,
        "businessTypeList": businessTypeList,
        "businessSourceTypeList": businessSourceTypeList,
        "warehouseIds": warehouseIds,
        "storeId": storeId,
        "supplierIds": supplierIds,
        "createTimeStart": createTimeStart if createTimeStart else taday,
        "createTimeEnd": createTimeEnd if createTimeEnd else taday,
        "submitTimeBegin": submitTimeBegin,
        "submitTimeEnd": submitTimeEnd,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "objectType": 3,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def outbound_post_goods(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    sort: Optional[str] = None,
    sortField: Optional[str] = None,
    outboundNo: Optional[str] = None,
    businessNo: Optional[str] = None,
    warehouseIds: Optional[List[str]] = None,
    goodsIdList: Optional[List[str]] = None,
    businessTypeList: Optional[List[int]] = None,
    storeId: Optional[str] = None,
    # ? 这里少了一个客户ID字段，类型是List[str]，可在 external_member_list 中获取
    businessSourceTypeList: Optional[List[int]] = None,
    createId: Optional[str] = None,
    supplierIds: Optional[List[str]] = None,
    createTimeStart: Optional[str] = None,
    createTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
        total: bool = False,) -> dict:
    """
    出库-出库单-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        sort (str, None): 排序方式. Defaults to None.
            - asc-升序
            - desc-降序
        sortField (str, None): 排序字段. Defaults to None.
        outboundNo (str, None): 出库单号. Defaults to None.
        businessNo (str, None): 业务单号. Defaults to None.
        warehouseIds (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        businessTypeList (List[int], None): 业务类型列表. Defaults to None.
            - 可在 out_bound_type 中获取，operateType=7
        storeId (str, None): 门店ID. Defaults to None.
            - 可在 select_store_warehouse 中获取
        supplierIds (List[str], None): 客户ID列表. Defaults to None.
            - 可在 external_member_list 中获取
        businessSourceTypeList (List[int], None): 业务来源类型列表. Defaults to None.
        createId (str, None): 制单人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        createTimeStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        total (bool, None): 是否查询汇总. Defaults to False.
            - True: 查询汇总
            - False: 查询分页数据
    Returns:
        dict: 出库-出库单-按商品响应体
    """
    if total:
        url = f"{base_url}/selectPostDetailsPageTotalSummary"
    else:
        url = f"{base_url}/selectPostDetailsPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "sort": sort,
        "sortField": sortField,
        "outboundNo": outboundNo,
        "businessNo": businessNo,
        "warehouseIds": warehouseIds,
        "goodsIdList": goodsIdList,
        "businessTypeList": businessTypeList,
        "storeId": storeId,
        "supplierIds": supplierIds,
        "businessSourceTypeList": businessSourceTypeList,
        "createId": createId,
        "createTimeStart": createTimeStart if createTimeStart else taday,
        "createTimeEnd": createTimeEnd if createTimeEnd else taday,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "objectType": 3,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
