"""
采购订单
    - 采购订单查询-当前机构-按订单: purchase_order
    - 采购订单详情-当前机构: purchase_order_details
    - 采购订单详情-当前机构-按商品查询: purchase_product_goods_details
    - 采购退货单-当前机构-按订单查询: purchase_return_order
    - 采购退货单详情-当前机构: purchase_return_order_detail
    - 采购退货单商品-当前机构-按商品查询: purchase_return_order_goods
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, retrieve_past_date


base_url = f"{yaoud_env['url']}/cp/goods"


async def purchase_order(
        authorization: str,
        tenant_id: int,
        current: int = 1,
        size: int = 20,
        status: Optional[List[str]] = None,
        createTimeStart: str = retrieve_past_date(1),
        createTimeEnd: Optional[str] = None,
        submitTimeStart: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        createName: Optional[str] = None,
        submitUserName: Optional[str] = None,
        salesDeptId: Optional[str] = None,
        purchaserId: Optional[str] = None,
        warehouseId: Optional[str] = None,
        customKeyword: Optional[str] = None,
        storeKeyword: Optional[str] = None,
        orderNo: Optional[str] = None,
        purchasePlanNo: Optional[str] = None,
        supplierCodeList: Optional[List[str]] = None,
        otherOrderNo: Optional[str] = None,
        businessNo: Optional[str] = None,) -> dict:
    """
    采购订单查询-当前机构-按订单
    Args:
        authorization (str): 认证信息
        tenant_id (int): 租户id
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        status (Optional[List[str]]): 订单状态列表. Defaults to None.
            - (1:草稿，2:审核中，3:待入库，4:已完成，5:已作废，6:已关闭)
        createTimeStart (str): 制单开始时间. Defaults to 前1天.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (Optional[str]): 制单结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeStart (Optional[str]): 提交开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (Optional[str]): 提交结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (Optional[str]): 生效开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (Optional[str]): 生效结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createName (Optional[str]): 制单人,支持模糊查找. Defaults to None.
        submitUserName (Optional[str]): 提交人,支持模糊查找. Defaults to None.
        salesDeptId (Optional[str]): 销售部门ID. Defaults to None.
        purchaserId (Optional[str]): 采购人ID. Defaults to None.
        warehouseId (Optional[str]): 仓库ID. Defaults to None.
        customKeyword (Optional[str]): 客户，用途未知. Defaults to None.
        storeKeyword (Optional[str]): 门店，用途未知. Defaults to None.
        orderNo (Optional[str]): 采购订单编码. Defaults to None.
        purchasePlanNo (Optional[str]): 采购计划编码. Defaults to None.
        supplierCodeList (Optional[List[str]]): 供应商编码列表. Defaults to None.
        otherOrderNo (Optional[str]): 三方单号. Defaults to None.
        businessNo (Optional[str]): 关联业务单号. Defaults to None.
    Returns:
        dict: 采购订单列表
    """
    url = f"{base_url}/indent/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id),
    }
    payload = {
        "current": current,  # 当前页码
        "size": size,  # 每页数量
        "status": status,
        "createTimeStart": createTimeStart,  # 制单开始时间
        "createTimeEnd": createTimeEnd,  # 制单结束时间
        "submitTimeStart": submitTimeStart,  # 提交开始时间
        "submitTimeEnd": submitTimeEnd,  # 提交结束时间
        "takeEffectTimeStart": takeEffectTimeStart,  # ? 生效开始时间,逻辑不明
        "takeEffectTimeEnd": takeEffectTimeEnd,  # ? 生效结束时间，逻辑不明
        "createName": createName,  # 制单人,支持模糊查找
        "submitUserName": submitUserName,  # 提交人,支持模糊查找
        "salesDeptId": salesDeptId,  # 销售部门ID
        "purchaserId": purchaserId,  # 采购人ID
        "warehouseId": warehouseId,  # 仓库ID
        "customKeyword": customKeyword,  # ? 客户，用途未知
        "storeKeyword": storeKeyword,  # ? 门店，用途未知
        "orderNo": orderNo,  # 采购订单编码
        "purchasePlanNo": purchasePlanNo,  # 采购计划编码
        "supplierCodeList": supplierCodeList,  # 供应商编码列表,默认是None,值类型为List[str]
        "otherOrderNo": otherOrderNo,  # 三方单号
        "businessNo": businessNo,  # 关联业务单号
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def purchase_order_details(
        authorization: str,
        purchase_order_id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    采购订单详情-当前机构
    Args:
        authorization (str): 授权token
        purchase_order_id (int): 采购订单ID
            - 在 purchase_order 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 采购订单详情
    """
    url = f"{base_url}/indent/info/{purchase_order_id}"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id),
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def purchase_product_goods_details(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        createTimeStart: str = retrieve_past_date(1),
        createTimeEnd: Optional[str] = None,
        submitTimeStart: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,
        orderNo: Optional[str] = None,
        supplierCodeList: Optional[List[str]] = None,
        goodsIdList: Optional[List[str]] = None,
        lineStatusType: Optional[str] = None,
        status: Optional[List[str]] = None,
        warehouseId: Optional[str] = None,
        purchaserId: Optional[str] = None,
        createName: Optional[str] = None,
        submitUserName: Optional[str] = None,
        selectRetailPrice: Optional[str] = None,
        storeKeyword: Optional[str] = None,
        customKeyword: Optional[str] = None, ) -> dict:
    """
    采购订单详情-当前机构-按商品查询
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        createTimeStart (str, None): 创建开始时间. Defaults to 前1天.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (Optional[str], None): 创建结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeStart (Optional[str], None): 提交开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (Optional[str], None): 提交结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (Optional[str], None): 生效开始时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (Optional[str], None): 生效结束时间. Defaults to None.
            - 日期格式为yyyy-MM-dd
        orderNo (Optional[str], None): 采购订单编码. Defaults to None.
        supplierCodeList (List[str], None): 供应商编码列表. Defaults to None.
        goodsIdList (List[str], None): 商品id列表. Defaults to None.
        lineStatusType (str, None): 行状态. Defaults to None.
            - (0:未入库， 1:已入库 2:部分入库)
        status (List[str], None): 单据状态. Defaults to None.
            - (1:草稿,2:审核中,3:待入库,4:已完成,5:已作废,6:已关闭)
        warehouseId (str, None): 收货仓库id. Defaults to None.
            - 可在 select_warehouse 中获取
        purchaserId (str, None): 采购员id. Defaults to None.
            - 可在 get_employee_list 中获取 postCodes=POST_BUYER。
        createName (str, None): 创建人姓名. Defaults to None.
        submitUserName (str, None): 提交人姓名. Defaults to None.
        selectRetailPrice (str, None): 仅显示采购价大于零售价，需过滤时填写true. Defaults to None.
        storeKeyword (str, None): 门店名称关键词 Defaults to None.
            - #! 用途未知
        customKeyword (str, None): 客户名称关键词. Defaults to None.
            - #! 用途未知
    Returns:
        dict: 采购订单商品详情
    """
    url = f"{base_url}/indent/d/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id),
    }
    params = {
        "current": current,
        "size": size,
        "createTimeStart": createTimeStart,  # 创建开始时间
        "createTimeEnd": createTimeEnd,  # 创建结束时间
        "submitTimeStart": submitTimeStart,  # 提交开始时间
        "submitTimeEnd": submitTimeEnd,  # 提交结束时间
        "takeEffectTimeStart": takeEffectTimeStart,  # ? 生效开始时间,逻辑不明
        "takeEffectTimeEnd": takeEffectTimeEnd,  # ? 生效结束时间，逻辑不明
        "orderNo": orderNo,  # 采购订单编码
        "supplierCodeList": supplierCodeList,  # 供应商编码列表
        "goodsIdList": goodsIdList,  # note 商品id列表,需要在goods_page_list中获取
        "lineStatusType": lineStatusType,  # 行状态,(0:未入库， 1:已入库 2:部分入库)
        "status": status,  # 单据状态，(1:草稿,2:审核中,3:待入库,4:已完成,5:已作废,6:已关闭)
        "warehouseId": warehouseId,  # 收货仓库id
        "purchaserId": purchaserId,  # 采购员id
        "createName": createName,  # 创建人姓名
        "submitUserName": submitUserName,  # 提交人姓名
        "selectRetailPrice": selectRetailPrice,  # 仅显示采购价大于零售价，需过滤时填写true
        "storeKeyword": storeKeyword,  # ? 门店名称关键词，逻辑未知
        "customKeyword": customKeyword,  # ? 客户名称关键词，逻辑未知
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def purchase_return_order(
    authorization: str,
    tenant_id: int,
    current: int = 1,
    pageSize: int = 20,
    orderNo: Optional[str] = None,
    purchaserId: Optional[int] = None,
    warehouseId: Optional[int] = None,
    status: Optional[List[int]] = None,
    supplierCodeList: Optional[List[str]] = None,
    createName: Optional[str] = None,
    submitUserName: Optional[str] = None,
    returnTypeValue: Optional[str] = None,
    createTimeStart: str = retrieve_past_date(1),
    createTimeEnd: Optional[str] = None,
    submitTimeStart: Optional[str] = None,
    submitTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    采购退货单-当前机构-按订单查询
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户id
        current (int): 当前页码. Defaults to 1.
        pageSize (int): 每页数量. Defaults to 20.
        orderNo (str,None): 退货单编号. Defaults to None.
        purchaserId (int, None): 采购员ID. Defaults to None.
            - 可在 get_employee_list 中获取 postCodes=POST_BUYER。
        warehouseId (int, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取。
        status (List[int],None): 退货单状态. Defaults to None.
            - (1:草稿，2:审批中，3:待出库，4:已完成，5:已作废，6:已关闭)
        supplierCodeList (List[str],None): 供应商编码列表. Defaults to None.
            - 可在 get_supplier_list 中获取
        createName (str,None): 制单人姓名. Defaults to None.
        submitUserName (str,None): 提交人姓名. Defaults to None.
        returnTypeValue (str,None): 退货类型. Defaults to None.
            - purchase_normal : 正常退货， purchase_recall : 召回退货
        createTimeStart (str,None): 制单时间区间-开始. Defaults to 前1天.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str,None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeStart (str,None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str,None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str,None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str,None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 采购退货单列表
    """
    url = f"{base_url}/return/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "pageSize": pageSize,
        "orderNo": orderNo,
        "purchaserId": purchaserId,
        "warehouseId": warehouseId,
        "status": status,
        "supplierCodeList": supplierCodeList,
        "createName": createName,
        "submitUserName": submitUserName,
        "returnTypeValue": returnTypeValue,
        "createTimeStart": createTimeStart,
        "createTimeEnd": createTimeEnd,
        "submitTimeStart": submitTimeStart,
        "submitTimeEnd": submitTimeEnd,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def purchase_return_order_detail(
    authorization: str,
    purchase_return_order_id: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    采购退货单详情-当前机构
    Args:
        authorization (str): 授权token
        purchase_return_order_id (int): 采购退货单ID
            - 在 purchase_return_order 中获取
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 采购退货单详情
    """
    url = f"{base_url}/return/info/{purchase_return_order_id}"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def purchase_return_order_goods(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    pageSize: int = 20,
    goodsIdList: Optional[List[str]] = None,
    purchaserId: Optional[int] = None,
    returnTypeValue: Optional[str] = None,
    warehouseId: Optional[int] = None,
    status: Optional[List[int]] = None,
    orderNo: Optional[str] = None,
    inboundNo: Optional[str] = None,
    batch: Optional[str] = None,
    batchNo: Optional[str] = None,
    reason: Optional[str] = None,
    createName: Optional[str] = None,
    submitUserName: Optional[str] = None,
    supplierCodeList: Optional[List[str]] = None,
    createTimeStart: str = retrieve_past_date(1),
    createTimeEnd: Optional[str] = None,
    submitTimeStart: Optional[str] = None,
    submitTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    采购退货单-当前机构-按商品查询
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户id
        current (int): 当前页码. Defaults to 1.
        pageSize (int): 每页数量. Defaults to 20.
        goodsIdList (List[str],None): 商品id列表. Defaults to None.
            - 可在 external_goods_page_llist 中获取ID.
        purchaserId (int,None): 采购员ID. Defaults to None.
            - 可在 get_employee_list 中获取 postCodes=POST_BUYER。
        returnTypeValue (str,None): 退货类型. Defaults to None.
            - (purchase_normal : 正常退货， purchase_recall : 召回退货)
        warehouseId (int,None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取。
        status (List[int],None): 退货单状态. Defaults to None.
            - (1:草稿，2:审批中，3:待出库，4:已完成，5:已作废，6:已关闭)
        orderNo (str,None): 退货单编号. Defaults to None.
        inboundNo (str,None): 入库单号. Defaults to None.
        batch (str,None): 批次号. Defaults to None.
        batchNo (str,None): 生产批号. Defaults to None.
        reason (str,None): 退货原因. Defaults to None.
        createName (str,None): 制单人姓名. Defaults to None.
        submitUserName (str,None): 提交人姓名. Defaults to None.
        supplierCodeList (List[str],None): 供应商编码列表. Defaults to None.
            - 可在 get_supplier_list 中获取
        createTimeStart (str,None): 制单时间区间-开始.日期格式为yyyy-MM-dd. Defaults to 前1天.
        createTimeEnd (str,None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeStart (str,None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str,None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str,None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str,None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 采购退货单商品详情
    """
    url = f"{base_url}/return/d/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "pageSize": pageSize,
        "goodsIdList": goodsIdList,
        "purchaserId": purchaserId,
        "returnTypeValue": returnTypeValue,
        "warehouseId": warehouseId,
        "status": status,
        "orderNo": orderNo,
        "inboundNo": inboundNo,
        "batch": batch,
        "batchNo": batchNo,
        "reason": reason,
        "createName": createName,
        "submitUserName": submitUserName,
        "supplierCodeList": supplierCodeList,
        "createTimeStart": createTimeStart,
        "createTimeEnd": createTimeEnd,
        "submitTimeStart": submitTimeStart,
        "submitTimeEnd": submitTimeEnd,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
