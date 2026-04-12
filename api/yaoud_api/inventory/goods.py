"""
商品管理
    - 门店商品/批次库存查询: store_stock_sum_batch
    - 仓库商品/批次库存查询: warehouse_stock
    - 仓库库存概况: warehouse_stock_overview
    - 出库-待出库: pending_outbound
    - 库存业务-业务类型查询-下拉检索用: out_bound_type
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/inventory/goods"
TTL = yaoud_env["timeout"]


async def store_stock_sum_batch(
        authorization: str,
        storeIdList: List[str],
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 50,
        filterZeroStock: bool = True,
        flag1: bool = False,
        flag2: bool = False,
        keywords: str = "",
        proAddress: Optional[str] = None,
        queryType: int = 0,
        cabinetIds: Optional[List[str]] = None,
        batch: Optional[str] = None,
        batchNo: Optional[str] = None,
        supplier: Optional[str] = None,
        productDateBegin: Optional[str] = None,
        productDateEnd: Optional[str] = None,
        effectiveDateBegin: Optional[str] = None,
        effectiveDateEnd: Optional[str] = None,
        inboundTimeBegin: Optional[str] = None,
        inboundTimeEnd: Optional[str] = None,
        title: int = 1) -> dict:
    """
    门店商品/批次库存查询
    Args:
        authorization (str): 授权token
            - 格式为"Bearer <token>"
        storeIdList (List[str]): 门店ID列表
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 每页数据数量. Defaults to 50.
        filterZeroStock (bool, None): 是否过滤库存为0的商品. Defaults to True.
        flag1 (bool, None): 是否过滤flag1. Defaults to False.
        flag2 (bool, None): 是否过滤flag2. Defaults to False.
        keywords (str, None): 搜索关键词. Defaults to "".
            - 商品编码/商品名称/通用名称/助记码/条码
        proAddress (str, None): 生产地址. Defaults to None.
        queryType (int, None): 查询类型.
            - （1:按批次查询；0:按商品查询）
        cabinetIds (List[str], None): 货柜ID列表.
            - queryType=1时可用
        batch (str, None): 批次.
            - queryType=1时可用
        batchNo (str, None): 生产批号.
            - queryType=1时可用
        supplier (str, None): 供应商编码.
            - queryType=1时可用
        productDateBegin (str, None): 生产日期区间-开始， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        productDateEnd (str, None): 生产日期区间-结束， Defaults to None.
            - queryType=1时可用
        effectiveDateBegin (str, None): 生效日期区间-开始， Defaults to None.
            - queryType=1时可用
        effectiveDateEnd (str, None): 生效日期区间-结束， Defaults to None.
            - queryType=1时可用
        inboundTimeBegin (str, None): 入库时间区间-开始， Defaults to None.
            - queryType=1时可用
        inboundTimeEnd (str, None): 入库时间区间-结束， Defaults to None.
            - queryType=1时可用
        title (int, None):未知参数. Defaults to 1.
    Returns:
        dict: 门店商品库存查询结果
    """

    url = f"{base_url}/report/storeStockSum"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    order_fields = [{"field": "split"}, {"field": "goodsCode", "order": "ascend"}, {"field": "commonName"}, {"field": "goodsName"}, {"field": "spec"}, {"field": "unit"}, {"field": "producer"}, {"field": "proAddress"}, {"field": "warehouseName"}, {"field": "allocationCode"}, {"field": "allocationName"}, {"field": "allocationTypeCn"}, {"field": "cabinetName"}, {"field": "stockQuantity"}, {
        "field": "avalilableQuantity"}, {"field": "costPrice"}, {"field": "amt"}, {"field": "taxRemovalAmt"}, {"field": "proPrice"}, {"field": "proMemberPrice"}, {"field": "supplierCode"}, {"field": "supplierName"}, {"field": "flag1"}, {"field": "flag2"}, {"field": "saleDept"}, {"field": "batch"}, {"field": "batchNo"}, {"field": "productDate"}, {"field": "expireDate"}, {"field": "warehouseTime"}]
    payload = {
        "storeIdList": storeIdList,  # 门店ID列表
        "current": current,
        "size": size,  # 每页数据数量，最大100
        "filterZeroStock": filterZeroStock,  # 是否过滤库存为0的商品
        "flag1": flag1,
        "flag2": flag2,
        "keywords": keywords,  # 搜索关键词: 商品编码/商品名称/通用名称/助记码/条码
        "proAddress": proAddress,  # 生产地址
        "queryType": queryType,  # 查询类型（1:按批次查询；0:按商品查询）
        "cabinetIds": cabinetIds,  # 货柜ID列表，queryType=1时可用
        "batch": batch,  # 批次，queryType=1时可用
        "batchNo": batchNo,  # 生产批号，queryType=1时可用
        "supplier": supplier,  # 供应商编码，queryType=1时可用
        "productDateBegin": productDateBegin,  # 生产日期-开始，queryType=1时可用
        "productDateEnd": productDateEnd,  # 生产日期-结束，queryType=1时可用
        "effectiveDateBegin": effectiveDateBegin,  # 生效日期-开始，queryType=1时可用
        "effectiveDateEnd": effectiveDateEnd,  # 生效日期-结束，queryType=1时可用
        "inboundTimeBegin": inboundTimeBegin,  # 入库时间-开始，queryType=1时可用
        "inboundTimeEnd": inboundTimeEnd,  # 入库时间-结束，queryType=1时可用
        "title": title,  # ? 未知参数
        "orderFields": order_fields
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def warehouse_stock(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 50,
        filterZeroStock: bool = True,
        keywords: str = "",
        queryType: int = 0,
        batch: Optional[str] = None,
        batchNo: Optional[str] = None,
        supplier: Optional[str] = None,
        productDateBegin: Optional[str] = None,
        productDateEnd: Optional[str] = None,
        effectiveDateBegin: Optional[str] = None,
        effectiveDateEnd: Optional[str] = None,
        inboundTimeBegin: Optional[str] = None,
        inboundTimeEnd: Optional[str] = None,
        warehouseList: Optional[List[str]] = None,) -> dict:
    """
    仓库商品/批次库存查询
    Args:
        authorization (str): 授权token
            - 格式为"Bearer <token>"
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 每页数据数量，最大100. Defaults to 50.
        filterZeroStock (bool, None): 是否过滤库存为0的商品. Defaults to True.
        keywords (str, None): 搜索关键词. Defaults to "".
            - 商品编码/商品名称/通用名称/助记码/条码
        queryType (int, None): 查询类型. Defaults to 0.
            - 0-按商品查询
            - 1-按批次查询
        batch (str, None): 批次， Defaults to None.
            - queryType=1时可用
        batchNo (str, None): 生产批号， Defaults to None.
            - queryType=1时可用
        supplier (str, None): 供应商编码， Defaults to None.
            - queryType=1时可用
        productDateBegin (str, None): 生产日期区间-开始， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        productDateEnd (str, None): 生产日期区间-结束， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        effectiveDateBegin (str, None): 生效日期区间-开始， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        effectiveDateEnd (str, None): 生效日期区间-结束， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        inboundTimeBegin (str, None): 入库时间区间-开始， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        inboundTimeEnd (str, None): 入库时间区间-结束， Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        warehouseList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
    Returns:
        dict: 仓库商品库存查询结果
    """
    url = f"{base_url}/report/warehouseStockSum"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,  # 每页数据数量，最大100
        "filterZeroStock": filterZeroStock,  # 是否过滤库存为0的商品
        "keywords": keywords,  # 搜索关键词: 商品编码/商品名称/通用名称/助记码/条码
        "queryType": queryType,  # 查询类型（1:按批次查询；0:按商品查询）
        "batch": batch,  # 批次，queryType=1时可用
        "batchNo": batchNo,  # 生产批号，queryType=1时可用
        "supplier": supplier,  # 供应商编码，queryType=1时可用
        "productDateBegin": productDateBegin,  # 生产日期-开始，queryType=1时可用
        "productDateEnd": productDateEnd,  # 生产日期-结束，queryType=1时可用
        "effectiveDateBegin": effectiveDateBegin,  # 生效日期-开始，queryType=1时可用
        "effectiveDateEnd": effectiveDateEnd,  # 生效日期-结束，queryType=1时可用
        "inboundTimeBegin": inboundTimeBegin,  # 入库时间-开始，queryType=1时可用
        "inboundTimeEnd": inboundTimeEnd,  # 入库时间-结束，queryType=1时可用
        "title": 1,  # 未知参数
        "warehouseList": warehouseList,  # 仓库ID列表
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def warehouse_stock_overview(
        authorization: str,
        tenant_id: Optional[int] = None,
        filterZeroStock: bool = True,
        keywords: str = "",
        queryType: int = 0,
        batch: Optional[str] = None,
        batchNo: Optional[str] = None,
        supplier: Optional[str] = None,
        productDateBegin: Optional[str] = None,
        productDateEnd: Optional[str] = None,
        effectiveDateBegin: Optional[str] = None,
        effectiveDateEnd: Optional[str] = None,
        inboundTimeBegin: Optional[str] = None,
        inboundTimeEnd: Optional[str] = None,
        title: int = 1,
        warehouseList: Optional[List[str]] = None,) -> dict:
    """
    仓库库存概况，可与 warehouse_stock 联动使用
    Args:
        authorization (str): 授权token，格式为"Bearer <token>"
        tenant_id (int, None): 租户ID. Defaults to None.
        filterZeroStock (bool, None): 是否过滤库存为0的商品. Defaults to True.
        keywords (str, None): 搜索关键词. Defaults to "".
            - 商品编码/商品名称/通用名称/助记码/条码
        queryType (int, None): 查询类型. Defaults to 0.
            - 0-按商品查询
            - 1-按批次查询
        batch (str, None): 批次. Defaults to None.
            - queryType=1时可用
        batchNo (str, None): 生产批号. Defaults to None.
            - queryType=1时可用
        supplier (str, None): 供应商编码. Defaults to None.
            - queryType=1时可用
        productDateBegin (str, None): 生产日期区间-开始. Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        productDateEnd (str, None): 生产日期区间-结束. Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        effectiveDateBegin (str, None): 生效日期区间-开始. Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        effectiveDateEnd (str, None): 生效日期区间-结束. Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        inboundTimeBegin (str, None): 入库时间区间-开始. Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        inboundTimeEnd (str, None): 入库时间区间-结束. Defaults to None.
            - queryType=1时可用
            - 日期格式为yyyy-MM-dd
        title (int, None): 未知参数. Defaults to 1.
        warehouseList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
    Returns:
        dict: 仓库库存概况结果
    """
    url = f"{base_url}/report/getWarehouseGoodsStockTitle"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "filterZeroStock": filterZeroStock,  # 是否过滤库存为0的商品
        "keywords": keywords,  # 搜索关键词: 商品编码/商品名称/通用名称/助记码/条码
        "queryType": queryType,  # 查询类型（1:按批次查询；0:按商品查询）
        "batch": batch,  # 批次，queryType=1时可用
        "batchNo": batchNo,  # 生产批号，queryType=1时可用
        "supplier": supplier,  # 供应商编码，queryType=1时可用
        "productDateBegin": productDateBegin,  # 生产日期-开始，queryType=1时可用
        "productDateEnd": productDateEnd,  # 生产日期-结束，queryType=1时可用
        "effectiveDateBegin": effectiveDateBegin,  # 生效日期-开始，queryType=1时可用
        "effectiveDateEnd": effectiveDateEnd,  # 生效日期-结束，queryType=1时可用
        "inboundTimeBegin": inboundTimeBegin,  # 入库时间-开始，queryType=1时可用
        "inboundTimeEnd": inboundTimeEnd,  # 入库时间-结束，queryType=1时可用
        "title": title,
        "warehouseList": warehouseList,  # 仓库ID列表
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def pending_outbound(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        status: Optional[int] = None,
        businessType: Optional[int] = None,
        createId: int = None,
        warehouseIds: Optional[List[str]] = None,
        businessNo: Optional[str] = None,
        sort: str = "asc",
        sortField: str = "submit_time",
        toWarehouseName: Optional[str] = None,
        submitId: Optional[int] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        submitTimeBegin: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,) -> dict:
    """
    出库-待出库
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        status (int, None): 单据状态. Defaults to None.
            - 1-待出库
            - 2-已关闭
        businessType (int, None): 业务类型. Defaults to None.
            - 可在 out_bound_type 中获取，operateType=7
        createId (int, None): 制单人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        warehouseIds (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        businessNo (str, None): 业务单号. Defaults to None.
        sort (str, None): 排序方式. Defaults to "asc".
            - asc-升序
            - desc-降序
        sortField (str, None): 排序字段. Defaults to "submit_time".
        toWarehouseName (str, None): 接收仓库名称. Defaults to None.
        submitId (int, None): 提交人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeBegin (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 出库-待出库响应体
    """
    url = f"{base_url}/treatOutbound/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createStartTime:
        create_start_time = get_date_start_and_end_time(createStartTime)
    else:
        taday = get_current_date()
        create_start_time = get_date_start_and_end_time(taday)
    if createEndTime:
        create_end_time = get_date_start_and_end_time(createEndTime)
    else:
        create_end_time = None
    if submitTimeBegin:
        submit_time_begin = get_date_start_and_end_time(submitTimeBegin)
    else:
        submit_time_begin = None
    if submitTimeEnd:
        submit_time_end = get_date_start_and_end_time(submitTimeEnd)
    else:
        submit_time_end = None
    params = {
        "current": current,
        "size": size,
        "status": status,
        "businessType": businessType,
        "createId": createId,
        "businessNo": businessNo,
        "sort": sort,
        "sortField": sortField,
        "toWarehouseName": toWarehouseName,
        "submitId": submitId,
        "createStartTime": create_start_time['start_time'] if create_start_time else None,
        "createEndTime": create_end_time['end_time'] if create_end_time else None,
        "submitTimeBegin": submit_time_begin['start_time'] if submit_time_begin else None,
        "submitTimeEnd": submit_time_end['end_time'] if submit_time_end else None,
        "objectType": 3,
        "_t": timestamp(),
    }
    # 如果warehouseIds不为空，则添加到params中
    #! 后端傻逼没写处理逻辑，只能手动处理
    if warehouseIds:
        params["warehouseIds"] = warehouseIds
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def out_bound_type(
        authorization: str,
        operateType: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    库存业务-业务类型查询-下拉检索用
    Args:
        authorization (str): 授权token
        operateType (int): 业务类型.
            - 7-待出库业务类型
            - 8-出库业务类型
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 库存业务-业务类型查询响应体
    """
    url = f"{base_url}/treatOutbound/dropDownToSelectOutboundType"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "objectType": 3,
        "operateType": operateType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
