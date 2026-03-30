"""
售后订单管理
    - 售后订单列表-退回: after_sale_page
    - 售后订单详情-退回: get_after_sale_by_id
    - 退款单查询: after_sale_refund
    - 退款单详情: after_sale_refund_detail
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/oms/afterSale"


async def after_sale_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        fieldType: int = 1,
        keyword: Optional[str] = None,
        applyStartDate: Optional[str] = None,
        applyEndDate: Optional[str] = None,
        orderSources: Optional[List[str]] = None,
        shopCodes: Optional[List[str]] = None,
        status: Optional[int] = None,
        type: Optional[int] = None,
        isReceiving: Optional[int] = None,
        isOutbound: Optional[int] = None,) -> dict:
    """
    获取售后订单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        fieldType (int): 字段类型. Defaults to 1.
            - 可选值：1-售后单号，2-下单手机，3-系统订单号，4-三方订单号，5-寄出快递单号，6-退回快递单号
        keyword (Optional[str]): 关键字，根据 fieldType 不同，搜索不同字段. Defaults to None.
        applyStartDate (Optional[str]): 申请开始区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        applyEndDate (Optional[str]): 申请结束区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        orderSources (Optional[List[str]]): 订单来源. Defaults to None.
            - 可在 dict_item_list 中获取 keyword="订单来源"
        shopCodes (Optional[List[str]]): 店铺编码. Defaults to None.
        status (Optional[int]): 状态. Defaults to None.
            - 可选值：None-全部，2-待审核，4-待退款，6-待入库，8-待处理，10-待换货，12-已换货，14-已关闭，16-已取消
        type (Optional[int]): 售后单类型. Defaults to None.
            - 可选值：1-仅退款，2-退货退款，3-换货
        isReceiving (Optional[int]): 是否入库. Defaults to None.
            - 可选值：1-已收货，0-未收货
        isOutbound (Optional[int]): 是否发货. Defaults to None.
            - 可选值：1-已发货，0-未发货
    Returns:
        dict: 售后订单列表
    """
    url = f"{base_url}/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if applyStartDate:
        apply_start_time = get_date_start_and_end_time(applyStartDate)
    else:
        taday = get_current_date()
        apply_start_time = get_date_start_and_end_time(taday)

    if applyEndDate:
        apply_end_time = get_date_start_and_end_time(applyEndDate)
    else:
        apply_end_time = None
    params = {
        "current": current,
        "size": size,
        "fieldType": fieldType,
        "keyword": keyword,
        "applyStartDate": apply_start_time['start_time'] if apply_start_time else None,
        "applyEndDate": apply_end_time['end_time'] if apply_end_time else None,
        "orderSources": orderSources,
        "shopCodes": shopCodes,
        "status": status,
        "type": type,
        "isReceiving": isReceiving,
        "isOutbound": isOutbound,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def get_after_sale_by_id(
        authorization: str,
        after_sale_id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    获取售后订单详情
    Args:
        authorization (str): 认证信息
        after_sale_id (str): 售后订单ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 售后订单详情
    """
    url = f"{base_url}/getAfterSaleById/{after_sale_id}"
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

async def after_sale_refund(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        fieldType: Optional[str] = None,
        refundNo: Optional[int] = None,
        orderId: Optional[int] = None,
        thirdPartyOrderId: Optional[int] = None,
        afterSaleNo: Optional[int] = None,
        buyerTelephone: Optional[str] = None,
        applyTimeStart: Optional[str] = None,
        applyTimeEnd: Optional[str] = None,
        orderSources: Optional[List[str]] = None,
        shopCodes: Optional[List[str]] = None,
        status: Optional[int] = None,) -> dict:
    """
    获取退款单查询
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        fieldType (str,None): 查询类型. Defaults to None.
            - 可选值：refundNo-退款单号，orderId-系统单号，thirdPartyOrderId-第三方单号，afterSaleNo-售后单号，buyerName-买家姓名
        refundNo (int,None): 退款单号. Defaults to None.
        orderId (int,None): 系统单号. Defaults to None.
        thirdPartyOrderId (int,None): 第三方单号. Defaults to None.
        afterSaleNo (int,None): 售后单号. Defaults to None.
        buyerTelephone (str,None): 买家电话. Defaults to None.
            - 仅针对线上订单
        applyTimeStart (str,None): 申请时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        applyTimeEnd (str,None): 申请时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        orderSources (List[str],None): 订单来源. Defaults to None.
            - 可在 dict_item_list 中获取 keyword="订单来源"
        shopCodes (List[str],None): 店铺编码. Defaults to None.
        status (int,None): 退款单状态. Defaults to None.
            - 可选值：2-待审核，4-待确认，5-待退款，6-退款中，8-退款失败，10-已关闭， 11-部分退款，12-退款成功
    Returns:
        dict: 退款单查询
    """
    url = f"{base_url}Refund/queryPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if applyTimeStart:
        apply_time_start = get_date_start_and_end_time(applyTimeStart)
    else:
        taday = get_current_date()
        apply_time_start = get_date_start_and_end_time(taday)
    if applyTimeEnd:
        apply_time_end = get_date_start_and_end_time(applyTimeEnd)
    else:
        apply_time_end = None
    params = {
        "current": current,
        "size": size,
        #! fieldType=None时，对应的参数一样能生效，脱裤子放屁
        "fieldType": fieldType,
        "refundNo": refundNo,
        "orderId": orderId,
        "thirdPartyOrderId": thirdPartyOrderId,
        "afterSaleNo": afterSaleNo,
        "buyerTelephone": buyerTelephone,
        "applyTimeStart": apply_time_start['start_time'] if apply_time_start else None,
        "applyTimeEnd": apply_time_end['end_time'] if apply_time_end else None,
        "orderSources": orderSources,
        "shopCodes": shopCodes,
        "status": status,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def after_sale_refund_detail(
        authorization: str,
        after_sale_refund_id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    获取退款单详情
    Args:
        authorization (str): 认证信息
        after_sale_refund_id (str): 退款单ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 退款单详情
    """
    url = f"{base_url}Refund/getAfterSaleRefundById/{after_sale_refund_id}"
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

