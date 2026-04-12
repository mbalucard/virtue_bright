"""
商品出库申请
    - 配送申请单列表: goods_apply_list
    - 配送申请单-详情: goods_apply_detail
    - 已转配送单单据列表-按单据: goods_distribution_list
    - 已转配送单单据列表-按商品明细: goods_distribution_details
    - 配送单详情: goods_distribution_info
    - 待分配商品列表: goods_wait_distribution
    - 待退仓单-按单据: goods_withdrawal_apply
    - 退仓申请单列表: return_request_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/distribution/dsGoods"



async def goods_apply_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    queryType: int = 0,
    status: Optional[int] = None,
    types: Optional[List[int]] = None,
    storeParam: Optional[str] = None,
    regionIdList: Optional[List[str]] = None,
    documentNo: Optional[str] = None,
    voucherName: Optional[str] = None,
    voucherTimeStart: Optional[str] = None,
    voucherTimeEnd: Optional[str] = None,
    submitStartTime: Optional[str] = None,
    submitEndTime: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
    goodsIdList: Optional[List[str]] = None,
    warehouseName: Optional[str] = None,) -> dict:
    """
    配送申请单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        queryType (int): 查询类型. Defaults to 0.
            - (0-按单据，1-按商品)
        status (int, None): 单据状态. Defaults to None.
            - (1-草稿，2-审批中，3-待批准，4-已完成，5-已关闭，6-已作废，7-已驳回)
        types (List[int], None): 单据类型. Defaults to None.
            - (1-正常请货，2-紧急请货，3-COP请货)
        storeParam (str, None): 收货门店编码. Defaults to None.
            - 可在 select_stores 中获取
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - 可在 store_region_tree 中获取
        documentNo (str, None): 单据编号. Defaults to None.
        voucherName (str, None): 制单人名称. Defaults to None.
        voucherTimeStart (str, None): 制单时间区间-开始. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        voucherTimeEnd (str, None): 制单时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        submitStartTime (str, None): 提交时间区间-开始,格式：yyyy-MM-dd. Defaults to None.
        submitEndTime (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 取货时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 取货时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        #! 当 queryType=1 时， 以下参数有效
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        warehouseName (str, None): 仓库名称. Defaults to None.
            - 支持模糊查找
    Returns:
        dict: 配送申请单列表
    """
    url = f"{base_url}Apply/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    # 时间格式转化，输出为YYYY-MM-DD hh:mm:ss
    if voucherTimeStart:
        start_time = get_date_start_and_end_time(voucherTimeStart)
    else:
        taday = get_current_date()
        start_time = get_date_start_and_end_time(taday)
    if voucherTimeEnd:
        end_time = get_date_start_and_end_time(voucherTimeEnd)
    else:
        end_time = None

    if submitStartTime:
        submit_start_time = get_date_start_and_end_time(submitStartTime)
    else:
        submit_start_time = None
    if submitEndTime:
        submit_end_time = get_date_start_and_end_time(submitEndTime)
    else:
        submit_end_time = None

    payload = {
        "current": current,
        "size": size,
        "queryType": queryType,
        "status": status,
        "types": types,
        "storeParam": storeParam,
        "regionIdList": regionIdList,
        "documentNo": documentNo,
        "voucherName": voucherName,
        "voucherTimeStart": start_time['start_time'] if start_time else None,
        "voucherTimeEnd": end_time['end_time'] if end_time else None,
        "submitStartTime": submit_start_time['start_time'] if submit_start_time else None,
        "submitEndTime": submit_end_time if submit_end_time else None,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "goodsIdList": goodsIdList,
        "warehouseName": warehouseName,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def goods_apply_detail(
    authorization: str,
    goods_apply_id: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    配送申请单-详情
    Args:
        authorization (str): 认证信息
        goods_apply_id (str): 配送申请单ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 配送申请单-详情
    """
    url = f"{base_url}Apply/detail/{goods_apply_id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def goods_distribution_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        businessTypeList: Optional[List[int]] = None,
        regionIdList: Optional[List[str]] = None,
        createIdList: Optional[List[str]] = None,
        deliveryMethodList: Optional[List[str]] = None,
        storeIdList: Optional[List[str]] = None,
        statusList: Optional[List[str]] = None,
        warehouseId: Optional[str] = None,
        storeType: Optional[int] = None,
        printed: Optional[int] = None,
        orderNo: Optional[str] = None,
        businessNo: Optional[str] = None,
        otherOrderNo: Optional[str] = None,
        remark: Optional[str] = None,
        createStartTime: str = get_current_date(),
        createEndTime: str = get_current_date(),
        submitStartTime: Optional[str] = None,
        submitEndTime: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    配送单-已转配送单单据列表-按单据
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页. Defaults to 1.
        size (int, optional): 每页条目数. Defaults to 10.
        businessTypeList (List[int], None): 单据类型. Defaults to None.
            - (1:正常请货单,2:铺货配送单,3:铺货配送单,4:期初配送单,5:调拨配送单,6:委托配送单,7:容售配货单,8:直配配送单,9:药诊配送单,10:紧急请货单,11:COP请货单,12:缺货配送单,13:缺货配送单)
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - List[str] 可在 store_region_tree 中获取
        createIdList (List[str], None): 制单人ID列表. Defaults to None.
            - List[str] 可在 get_employee_list 中获取
        deliveryMethodList (List[str], None): 配送方式列表. Defaults to None.
            - List[str],(distribution_way:配送,consignment_way:托运，self_pickup_way:自提)
        storeIdList (List[str], None): 收货门店ID. Defaults to None.
            - List[str] 可在 select_stores 中获取
        statusList (List[str], None): 状态列表. Defaults to None.
            - List[str] (1:草稿，2:审批中，3:待仓库出库，8:待门店入库，4:已完成，5:已作废，6:已关闭，7:已驳回)
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取
        storeType (int, None): 门店类型. Defaults to None.
            - (1:直营，2:加盟)
        submitStartTime (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitEndTime (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 配送单-已转配送单单据列表
    """
    url = f"{base_url}Distribution/selectPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "businessTypeList": businessTypeList,
        "regionIdList": regionIdList,
        "createIdList": createIdList,
        "deliveryMethodList": deliveryMethodList,
        "storeIdList": storeIdList,
        "statusList": statusList,
        "warehouseId": warehouseId,
        "storeType": storeType,
        "printed": printed,
        "orderNo": orderNo,
        "businessNo": businessNo,
        "otherOrderNo": otherOrderNo,
        "remark": remark,
        "createStartTime": createStartTime,
        "createEndTime": createEndTime,
        "submitStartTime": submitStartTime,
        "submitEndTime": submitEndTime,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def goods_distribution_details(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        businessTypeList: Optional[List[int]] = None,
        regionIdList: Optional[List[str]] = None,
        createIdList: Optional[List[str]] = None,
        deliveryMethodList: Optional[List[str]] = None,
        storeIdList: Optional[List[str]] = None,
        goodsIdList: Optional[List[str]] = None,
        statusList: Optional[List[str]] = None,
        warehouseId: Optional[str] = None,
        storeType: Optional[int] = None,
        orderNo: Optional[str] = None,
        businessNo: Optional[str] = None,
        otherOrderNo: Optional[str] = None,
        remark: Optional[str] = None,
        createStartTime: str = get_current_date(),
        createEndTime: str = get_current_date(),
        submitStartTime: Optional[str] = None,
        submitEndTime: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    配送单-已转配送单单据列表-按商品明细
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页. Defaults to 1.
        size (int, optional): 每页条目数. Defaults to 10.
        businessTypeList (List[int], None): 单据类型. Defaults to None.
            - (1:正常请货单,2:铺货配送单,3:铺货配送单,4:期初配送单,5:调拨配送单,6:委托配送单,7:容售配货单,8:直配配送单,9:药诊配送单,10:紧急请货单,11:COP请货单,12:缺货配送单,13:缺货配送单)
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - List[str] 可在 store_region_tree 中获取
        createIdList (List[str], None): 制单人ID列表. Defaults to None.
            - List[str] 可在 get_employee_list 中获取
        deliveryMethodList (List[str], None): 配送方式列表. Defaults to None.
            - List[str],(distribution_way:配送,consignment_way:托运，self_pickup_way:自提)
        storeIdList (List[str], None): 收货门店ID. Defaults to None.
            - List[str] 可在 select_stores 中获取
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
            - List[str] 可在 select_goods 中获取
        statusList (List[str], None): 状态列表. Defaults to None.
            - List[str] (1:草稿，2:审批中，3:待仓库出库，8:待门店入库，4:已完成，5:已作废，6:已关闭，7:已驳回)
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取
        storeType (int, None): 门店类型. Defaults to None.
            - (1:直营，2:加盟)
        orderNo (str, None): 配送单号. Defaults to None.
        businessNo (str, None): 关联业务单号. Defaults to None.
        otherOrderNo (str, None): 第三方单号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        createStartTime (str, None): 制单时间区间-开始. Defaults to 当前日期.
        submitStartTime (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitEndTime (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 配送单-已转配送单单据列表-按商品明细
    """
    url = f"{base_url}Distribution/detail/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "businessTypeList": businessTypeList,
        "regionIdList": regionIdList,
        "createIdList": createIdList,
        "deliveryMethodList": deliveryMethodList,
        "storeIdList": storeIdList,
        "goodsIdList": goodsIdList,
        "statusList": statusList,
        "warehouseId": warehouseId,
        "storeType": storeType,
        "orderNo": orderNo,
        "businessNo": businessNo,
        "otherOrderNo": otherOrderNo,
        "remark": remark,
        "createStartTime": createStartTime,
        "createEndTime": createEndTime,
        "submitStartTime": submitStartTime,
        "submitEndTime": submitEndTime,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def goods_distribution_info(
        authorization: str,
        order_number: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    配送单详情
    Args:
        authorization (str): 认证信息
        order_number (str): 配送单号
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 配送单详情
    """
    url = f"{base_url}Distribution/info/{order_number}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": order_number,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def goods_wait_distribution(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        businessNo: Optional[str] = None,
        warehouseId: Optional[str] = None,
        remark: Optional[str] = None,
        businessTypeList: Optional[List[str]] = None,
        deliveryMethod: Optional[str] = None,
        regionIdList: Optional[List[int]] = None,
        tagIdList: Optional[List[int]] = None,
        storeIdList: Optional[List[str]] = None,
        objectIds: Optional[List[str]] = None,
        createId: Optional[str] = None,
        createStartTime: str = get_current_date(),
        createEndTime: str = get_current_date(),) -> dict:
    """
    配送单-待配送
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页. Defaults to 1.
        size (int, optional): 每页条目数最大100. Defaults to 10.
        businessNo (str, None): 关联业务单号. Defaults to None.
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取.
        remark (str, None): 备注. Defaults to None.
        businessTypeList (List[str], None): 单据类型. Defaults to None.
            - List[int], (1:正常清货，2:铺货配送，3:紧急清货，4:COP清货）
        deliveryMethod (str, None): 配送方式. Defaults to None.
            - (distribution_way:配送,consignment_way:托运，self_pickup_way:自提)
        regionIdList (List[int], None): 区域ID列表. Defaults to None.
            - List[str] 可在 store_region_tree 中获取.
        tagIdList (List[int], None): 标签ID列表. Defaults to None.
            - 可在 item_list 中获取 objType="store_management".
        storeIdList (List[str], None): 收货门店ID列表. Defaults to None.
            - 可在 select_stores 中获取.
        objectIds (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取.
        createId (str, None): 制单人ID. Defaults to None.
            - 可在 get_employee_list 中获取.
        createStartTime (str, None): 制单时间区间-开始. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 配送单-待配送单列表
    """
    url = f"{base_url}WaitDistribution/selectPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "businessNo": businessNo,
        "warehouseId": warehouseId,
        "remark": remark,
        "businessTypeList": businessTypeList,
        "deliveryMethod": deliveryMethod,
        "regionIdList": regionIdList,
        "tagIdList": tagIdList,
        "storeIdList": storeIdList,
        "objectIds": objectIds,
        "createId": createId,
        "createStartTime": createStartTime,
        "createEndTime": createEndTime,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def goods_withdrawal_apply(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        field: Optional[str] = "createTime",
        order: Optional[str] = "asc",
        retType: int = 1,
        documentNo: Optional[str] = None,
        warehouseIds: Optional[List[int]] = None,
        storeIds: Optional[List[int]] = None,
        stoType: Optional[int] = None,
        objectIds: Optional[List[int]] = None,
        createIds: Optional[List[int]] = None,) -> dict:
    """
    待退仓单-按单据
    #! 无数据，暂未验证此接口。
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 10.
        retType (int): 退仓类型, 用途未知. Defaults to 1.
            - 用途未知
        field (str, optional): 排序字段. Defaults to "createTime".
            - createTime表示制单时间
        order (str, optional): 排序方向. Defaults to "asc".
            - asc表示升序，desc表示降序
        documentNo (str, None): 关联单号. Defaults to None.
        warehouseIds (List[int], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        storeIds (List[int], None): 门店ID列表. Defaults to None.
            - 可在 select_stores 中获取
        stoType (int, None): 门店类型. Defaults to None.
            - (1-直营，2-加盟)
        objectIds (List[int], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        createIds (List[int], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
    Returns:
        dict: 待退仓单-按单据
    """
    url = f"{base_url}WithdrawalApply/wait/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "retType": retType,
        "field": field,
        "order": order,
        "documentNo": documentNo,
        "warehouseIds": warehouseIds,
        "storeIds": storeIds,
        "stoType": stoType,
        "objectIds": objectIds,
        "createIds": createIds,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def return_request_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    queryType: int = 0,
    field: Optional[str] = "createTime",
    order: Optional[str] = "desc",
    status: Optional[int] = None,
    documentNo: Optional[str] = None,
    storeParam: Optional[str] = None,
    voucherName: Optional[str] = None,
    voucherTimeStart: Optional[str] = None,
    voucherTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
    goodsIdList: Optional[List[str]] = None,) -> dict:
    """
    退仓申请单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        queryType (int): 查询类型. Defaults to 0.
            - (0-按单据，1-按商品)
        field (str, optional): 排序字段. Defaults to "createTime".
            - createTime表示制单时间
        order (str, optional): 排序方向. Defaults to "desc".
            - desc表示降序，asc表示升序
        status (int, None): 单据状态. Defaults to None.
            - (1-草稿，2-审批中，5-待批准，3-已完成，4-已作废，6-已关闭，7-已驳回)
        documentNo (str, None): 单据编号. Defaults to None.
        storeParam (str, None): 退仓门店编码. Defaults to None.
            - 可在 select_stores 中获取
        voucherName (str, None): 制单人姓名. Defaults to None.
        voucherTimeStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        voucherTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        #! 当 queryType=1 时， 以下参数有效
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
    Returns:
        dict: 退仓申请单列表
    """
    url = f"{base_url}WithdrawalApply/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    # 时间格式转化，输出为YYYY-MM-DD hh:mm:ss
    if voucherTimeStart:
        start_time = get_date_start_and_end_time(voucherTimeStart)
    else:
        taday = get_current_date()
        start_time = get_date_start_and_end_time(taday)
    if voucherTimeEnd:
        end_time = get_date_start_and_end_time(voucherTimeEnd)
    else:
        end_time = None

    if takeEffectTimeStart:
        takeEffect_start_time = get_date_start_and_end_time(
            takeEffectTimeStart)
    else:
        takeEffect_start_time = None
    if takeEffectTimeEnd:
        takeEffect_end_time = get_date_start_and_end_time(takeEffectTimeEnd)
    else:
        takeEffect_end_time = None
    payload = {
        "current": current,
        "size": size,
        "queryType": queryType,
        "field": field,
        "order": order,
        "status": status,
        "documentNo": documentNo,
        "storeParam": storeParam,
        "voucherName": voucherName,
        "voucherTimeStart": start_time['start_time'] if start_time else None,
        "voucherTimeEnd": end_time['end_time'] if end_time else None,
        "takeEffectTimeStart": takeEffect_start_time['start_time'] if takeEffect_start_time else None,
        "takeEffectTimeEnd": takeEffect_end_time['end_time'] if takeEffect_end_time else None,
        "goodsIdList": goodsIdList,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
