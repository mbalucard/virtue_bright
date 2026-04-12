"""
库存管理
    - 入库单-当前机构-按订单: iv_in_bound_list_bill
    - 入库单-当前机构-订单详情: warehouse_receipt_details
    - 入库单-当前机构-按商品: warehouse_receipt_goods
    - 零售占用单据查询- OMS: oms_stock_lock_list
    - 批次调整-按单据: batch_adjust_page
    - 批次调整-按商品: batch_adjust_detail_page
    - 批号盘点-按单据: batch_no_inventory_page
    - 批号盘点-按商品: batch_no_inventory_detail
    - 货位调整-按单据: adjust_shelf_page
    - 货位调整-按单据-明细: adjust_shelf_detail
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, retrieve_past_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/inventory/iv"


async def warehouse_receipt(
        authorization: str,
        tenant_id: int,
        current: int = 1,
        size: int = 20,
        businessSourceTypeList: Optional[List[int]] = None,
        businessTypeList: Optional[List[int]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        objectType: int = 3,
        warehouseCodeList: Optional[List[str]] = None,
        sort: str = "",
        sortField: str = "",
        businessNo: Optional[str] = None,
        createName: Optional[str] = None,
        goodsIdList: Optional[List[str]] = None,
        printed: Optional[int] = None,
        otherOrder: Optional[str] = None,
        upstreamSaleOrderNo: Optional[str] = None,
        upstreamSaleDate: Optional[str] = None,
        inboundNo: Optional[str] = None,
        remark: Optional[str] = None,) -> dict:
    """
    入库单-当前机构-按订单
    Args:
        authorization (str): 授权token，格式为"Bearer <token>"
        tenant_id (int): 租户ID
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        businessSourceTypeList (List[int], None): 业务来源类型列表. Defaults to None.
            - 15:采购，8:药诊补单，6:调拨补单，18：外部调拨，3:配送单，4：退仓单， 11:内部委托配送， 1:外部委托配送
        businessTypeList (List[int], None): 入库类型列表. Defaults to None.
            - 1:采购单，3:退仓单,4:配送拒收入库单， 12:报溢入库单， 14:盘盈入库， 13:货位调整入库单，15:成本调整入库单，20:批发退货入库单
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        objectType (int, None): 未知参数. Defaults to 3.
        warehouseCodeList (List[str], None): 仓库编码列表. Defaults to None.
        sort (str, None): 排序方向. Defaults to "".
        sortField (str, None): 排序字段. Defaults to "".
        businessNo (str, None): 关联业务单号. Defaults to None.
        createName (str, None): 制单人姓名. Defaults to None.
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
        printed (int, None): 打印状态. Defaults to None.
            - 1-已打印
            - 0-未打印
        otherOrder (str, None): 三方单号. Defaults to None.
        upstreamSaleOrderNo (str, None): 上游销售订单号. Defaults to None.
        upstreamSaleDate (str, None): 上游销售日期. Defaults to None.
            - 日期格式为yyyy-MM-dd
        inboundNo (str, None): 入库单号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
    Returns:
        dict: 入库单-按订单结果
    """
    url = f"{base_url}InBound/listBill"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id),  # 租户ID 必填
    }
    payload = {
        "current": current,  # 当前页码
        "size": size,    # 每页数量
        "businessSourceTypeList": businessSourceTypeList,
        "businessTypeList": businessTypeList,
        # 制单开始时间
        "createTimeBegin": createTimeBegin if createTimeBegin else retrieve_past_date(1),
        "createTimeEnd": createTimeEnd,  # 制单结束时间
        "takeEffectTimeStart": takeEffectTimeStart,  # 生效开始时间
        "takeEffectTimeEnd": takeEffectTimeEnd,  # 生效结束时间
        "objectType": objectType,  # ? 未知参数
        "warehouseCodeList": warehouseCodeList,  # 仓库编码列表，数据类型 List[str] | None
        "sort": sort,  # ? 排序方向,暂时无用
        "sortField": sortField,  # ? 排序字段，暂时无用
        "businessNo": businessNo,  # 关联业务单号
        "createName": createName,  # 制单人姓名
        "goodsIdList": goodsIdList,  # 商品ID,类型 List[str] | None
        "printed": printed,  # 打印状态（1:已打印，0:未打印）
        "otherOrder": otherOrder,  # 三方单号
        "upstreamSaleOrderNo": upstreamSaleOrderNo,  # 上游销售订单号
        "upstreamSaleDate": upstreamSaleDate,  # 上游销售日期,格式 yyyy-MM-dd
        "inboundNo": inboundNo,  # 入库单号
        "remark": remark  # 备注
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def warehouse_receipt_details(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    入库单-当前机构-订单详情
    Args:
        authorization (str): 授权token
        id (str): 入库单ID,
            - 可在 warehouse_receipt 中获取
        tenant_id (int, None): 租户ID. Defaults to None.  
    Returns:
        dict: 入库单-订单详情响应体
    """
    url = f"{base_url}InBound/getBillById"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "id": id,  # 入库单ID
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def warehouse_receipt_goods(
        authorization: str,
        tenant_id: int,
        current: int = 1,
        size: int = 20,
        businessSourceTypeList: Optional[List[int]] = None,
        businessTypeList: Optional[List[int]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        objectType: int = 3,
        warehouseCodeList: Optional[List[str]] = None,
        sort: str = "",
        sortField: str = "",
        businessNo: Optional[str] = None,
        createName: Optional[str] = None,
        goodsIdList: Optional[List[str]] = None,
        otherOrder: Optional[str] = None,
        upstreamSaleOrderNo: Optional[str] = None,
        upstreamSaleDate: Optional[str] = None,
        inboundNo: Optional[str] = None,
        batch: Optional[str] = None,
        batchNo: Optional[str] = None,
        producer: Optional[str] = None,
        remark: Optional[str] = None,):
    """
    入库单-当前机构-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户ID
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        businessSourceTypeList (List[int], None): 业务来源类型列表. Defaults to None.
            - 15:采购，8:药诊补单，6:调拨补单，18：外部调拨，3:配送单，4：退仓单， 11:内部委托配送， 1:外部委托配送
        businessTypeList (List[int], None): 入库类型列表. Defaults to None.
            - 1:采购单，3:退仓单,4:配送拒收入库单， 12:报溢入库单， 14:盘盈入库， 13:货位调整入库单，15:成本调整入库单，20:批发退货入库单
        createTimeBegin (str, None): 制单开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        objectType (int, None): ? 未知参数. Defaults to 3.
        warehouseCodeList (List[str], None): 仓库编码列表. Defaults to None.
        printed (int, None): 打印状态. Defaults to None.
            - 1-已打印
            - 0-未打印
        businessNo (str, None): 关联业务单号. Defaults to None.
        createName (str, None): 制单人姓名. Defaults to None.
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
        otherOrder (str, None): 三方单号. Defaults to None.
        upstreamSaleOrderNo (str, None): 上游销售订单号. Defaults to None.
        upstreamSaleDate (str, None): 上游销售日期. Defaults to None.
            - 日期格式为yyyy-MM-dd
        inboundNo (str, None): 入库单号. Defaults to None.
        batch (str, None): 批次号. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        producer (str, None): 生产商. Defaults to None.
        remark (str, None): 备注. Defaults to None.
    Returns:
        dict: 入库单-按商品响应体
    """
    url = f"{base_url}InBoundD/listDetail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id),  # 租户ID 必填
    }
    payload = {
        "current": current,  # 当前页码
        "size": size,    # 每页数量
        "businessSourceTypeList": businessSourceTypeList,
        "businessTypeList": businessTypeList,
        # 制单开始时间
        "createTimeBegin": createTimeBegin if createTimeBegin else retrieve_past_date(1),
        "createTimeEnd": createTimeEnd,  # 制单结束时间
        "takeEffectTimeStart": takeEffectTimeStart,  # 生效开始时间
        "takeEffectTimeEnd": takeEffectTimeEnd,  # 生效结束时间
        "objectType": objectType,  # ? 未知参数
        "warehouseCodeList": warehouseCodeList,  # 仓库编码列表，数据类型 List[str] | None
        "sort": sort,  # ? 排序方向,暂时无用
        "sortField": sortField,  # ? 排序字段，暂时无用
        "businessNo": businessNo,  # 关联业务单号
        "createName": createName,  # 制单人姓名
        "goodsIdList": goodsIdList,  # 商品ID,类型 List[str] | None
        "otherOrder": otherOrder,  # 三方单号
        "upstreamSaleOrderNo": upstreamSaleOrderNo,  # 上游销售订单号
        "upstreamSaleDate": upstreamSaleDate,  # 上游销售日期,格式 yyyy-MM-dd
        "inboundNo": inboundNo,  # 入库单号
        "batch": batch,  # 批次号
        "batchNo": batchNo,  # 生产批号
        "producer": producer,  # 生产企业
        "remark": remark  # 备注
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def oms_stock_lock_list(
        authorization: str,
        tenant_id: int,
        warehouseId: str,
        current: int = 1,
        size: int = 20,
        sortType: int = 2,
        startTimeStr: Optional[str] = None,
        endTimeStr: Optional[str] = None,
        upstreamBusinessId: Optional[str] = None,
        businessNo: Optional[str] = None,) -> dict:
    """
    零售占用单据查询- OMS
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户ID
        warehouseId (str): 仓库ID, 仓库ID可在 warehouse_info_list 中获取
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        sortType (int, None): 排序类型. Defaults to 2.
        startTimeStr (str, None): 开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        endTimeStr (str, None): 结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        upstreamBusinessId (str, None): 上游业务单号. Defaults to None.
        businessNo (str, None): 占用单号. Defaults to None.
    Returns:
        dict: 零售占用单据查询- OMS响应体
    """
    url = f"{base_url}StockLock/selectStockLockListByOms"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id),
    }
    if startTimeStr:
        start_time = get_date_start_and_end_time(startTimeStr)
    else:
        taday = get_current_date()
        start_time = get_date_start_and_end_time(taday)
    if endTimeStr:
        end_time = get_date_start_and_end_time(endTimeStr)
    else:
        end_time = None

    payload = {
        "current": current,
        "size": size,
        "sortType": sortType,  # ? 排序类型,用处未知
        "startTimeStr": start_time["start_time"] if start_time else None,
        "endTimeStr": end_time["end_time"] if end_time else None,
        "warehouseId": warehouseId,
        "upstreamBusinessId": upstreamBusinessId,
        "businessNo": businessNo,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def batch_adjust_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        orderNo: Optional[str] = None,
        createName: Optional[str] = None,
        status: Optional[int] = None,
        createTimeStart: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    批次调整-按单据
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        orderNo (str, None): 单据号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        status (int, None): 单据状态. Defaults to None.
            - 可选值：1-草稿 2-审批中 3-已完成 4-已作废 5-已关闭 7-已驳回
        createTimeStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}/batch/info/adjust/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "orderNo": orderNo,
        "createName": createName,
        "status": status,
        "createTimeStart": createTimeStart if createTimeStart else get_current_date(),
        "createTimeEnd": createTimeEnd if createTimeEnd else get_current_date(),
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "objectType": 3,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def batch_adjust_detail_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        name: Optional[str] = None,
        orderNo: Optional[str] = None,
        batch: Optional[str] = None,
        batchNo: Optional[str] = None,
        batchSterilization: Optional[str] = None,
        status: Optional[int] = None,
        createTimeStart: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        productDateStart: Optional[str] = None,
        productDateEnd: Optional[str] = None,
        expiryDateStart: Optional[str] = None,
        expiryDateEnd: Optional[str] = None,
        sterilizationDateStart: Optional[str] = None,
        sterilizationDateEnd: Optional[str] = None,
        sterilizationExpireDateStart: Optional[str] = None,
        sterilizationExpireDateEnd: Optional[str] = None,) -> dict:
    """
    批次调整-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        name (str, None): 商品名称. Defaults to None.
        orderNo (str, None): 单据号. Defaults to None.
        batch (str, None): 批次号. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        batchSterilization (str, None): 灭菌批号. Defaults to None.
        status (int, None): 单据状态. Defaults to None.
            - 可选值：1-草稿 2-审批中 3-已完成 4-已作废 5-已关闭 7-已驳回

        createTimeStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        productDateStart (str, None): 生产日期区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        productDateEnd (str, None): 生产日期区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        expiryDateStart (str, None): 有效期区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        expiryDateEnd (str, None): 有效期区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sterilizationDateStart (str, None): 灭菌日期区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sterilizationDateEnd (str, None): 灭菌日期区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sterilizationExpireDateStart (str, None): 灭菌有效期区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sterilizationExpireDateEnd (str, None): 灭菌有效期区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    """
    url = f"{base_url}/batch/info/adjust/d/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "name": name,
        "orderNo": orderNo,
        "batch": batch,
        "batchNo": batchNo,
        "batchSterilization": batchSterilization,
        "status": status,
        "createTimeStart": createTimeStart if createTimeStart else get_current_date(),
        "createTimeEnd": createTimeEnd if createTimeEnd else get_current_date(),
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "productDateStart": productDateStart,
        "productDateEnd": productDateEnd,
        "expiryDateStart": expiryDateStart,
        "expiryDateEnd": expiryDateEnd,
        "sterilizationDateStart": sterilizationDateStart,
        "sterilizationDateEnd": sterilizationDateEnd,
        "sterilizationExpireDateStart": sterilizationExpireDateStart,
        "sterilizationExpireDateEnd": sterilizationExpireDateEnd,
        "objectType": 3,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def batch_no_inventory_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    documentNo: Optional[str] = None,
    createName: Optional[str] = None,
    createDateStart: Optional[str] = None,
    createDateEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    批号盘点-按单据
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNo (str, None): 单据号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        createDateStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createDateEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 批号盘点-按单据响应体
    """
    url = f"{base_url}BatchNoInventory/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "documentNo": documentNo,
        "createName": createName,
        "createDateStart": createDateStart if createDateStart else get_current_date(),
        "createDateEnd": createDateEnd if createDateEnd else get_current_date(),
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def batch_no_inventory_detail(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    documentNo: Optional[str] = None,
    createName: Optional[str] = None,
    keyWords: Optional[str] = None,
    batch: Optional[str] = None,
    batchNo: Optional[str] = None,
    batchSterilizationNo: Optional[str] = None,
    warehouseIdList: Optional[List[str]] = None,
    allocationId: Optional[int] = None,
    createDateStart: Optional[str] = None,
    createDateEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
    sterilizationExpireDateStart: Optional[str] = None,
    sterilizationExpireDateEnd: Optional[str] = None,)->dict:
    """
    批号盘点-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNo (str, None): 单据号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        keyWords (str, None): 商品关键字检索. Defaults to None.
        batch (str, None): 批次号. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        batchSterilizationNo (str, None): 灭菌批号. Defaults to None.
        warehouseIdList (List[str], None): 仓库ID. Defaults to None.
            - 可在 ent_store_warehouse_query 中获取，对应字段id
        allocationId (int, None): 货位ID. Defaults to None.
            - 可在 warehouse_location_list 中获取
        createDateStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createDateEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sterilizationExpireDateStart (str, None): 灭菌有效期区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sterilizationExpireDateEnd (str, None): 灭菌有效期区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 批号盘点-按商品响应体
    """
    url = f"{base_url}BatchNoInventoryDtl/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "documentNo": documentNo,
        "createName": createName,
        "keyWords": keyWords,
        "batch": batch,
        "batchNo": batchNo,
        "batchSterilizationNo": batchSterilizationNo,
        "warehouseIdList": warehouseIdList,
        "allocationId": allocationId if warehouseIdList else None,
        "createDateStart": createDateStart if createDateStart else get_current_date(),
        "createDateEnd": createDateEnd if createDateEnd else get_current_date(),
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "sterilizationExpireDateStart": sterilizationExpireDateStart,
        "sterilizationExpireDateEnd": sterilizationExpireDateEnd,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def adjust_shelf_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    businessNo: Optional[str] = None,
    moveNo: Optional[str] = None,
    createName: Optional[str] = None,
    submitName: Optional[str] = None,
    warehouseId: Optional[int] = None,
    createTimeStart: Optional[str] = None,
    createTimeEnd: Optional[str] = None,
    submitTimeBegin: Optional[str] = None,
    submitTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    货位调整-按单据
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        businessNo (str, None): 单据号. Defaults to None.
        moveNo (str, None): 关联WMS单号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        submitName (str, None): 提交人. Defaults to None.
        warehouseId (int, None): 仓库,门店,诊所ID. Defaults to None.
            - 可在 location_control_warehouse_stores 中获取
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
    Returns:
        dict: 货位调整-按单据响应体
    """
    url = f"{base_url}AdjustShelf/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "businessNo": businessNo,
        "moveNo": moveNo,
        "createName": createName,
        "submitName": submitName,
        "warehouseId": warehouseId,
        "createTimeStart": createTimeStart if createTimeStart else get_current_date(),
        "createTimeEnd": createTimeEnd if createTimeEnd else get_current_date(),
        "submitTimeBegin": submitTimeBegin,
        "submitTimeEnd": submitTimeEnd,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "businessType": 3,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def adjust_shelf_detail(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    businessNo: Optional[str] = None,
    moveNo: Optional[str] = None,
    goodsCode: Optional[str] = None,
    createName: Optional[str] = None,
    warehouseId: Optional[int] = None,
    createTimeStart: Optional[str] = None,
    createTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    货位调整-按单据-明细
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        businessNo (str, None): 单据号. Defaults to None.
        moveNo (str, None): 关联WMS单号. Defaults to None.
        goodsCode (str, None): 商品编码. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        warehouseId (int, None): 仓库,门店,诊所ID. Defaults to None.
            - 可在 location_control_warehouse_stores 中获取
        createTimeStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 货位调整-按单据响应体
    """
    url = f"{base_url}AdjustShelfD/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "businessNo": businessNo,
        "moveNo": moveNo,
        "goodsCode": goodsCode,
        "createName": createName,
        "warehouseId": warehouseId,
        "createTimeStart": createTimeStart if createTimeStart else get_current_date(),
        "createTimeEnd": createTimeEnd if createTimeEnd else get_current_date(),
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "businessType":3,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
