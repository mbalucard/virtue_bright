"""
支付
    - 可用支付方式-下拉检索用: payment_method_query
    - 门店支付方式-下拉检索用: store_payment_method
    - 支付状态-下拉检索用: payment_record_index
    - 零售收款单/退款单查询: payment_record_page
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/payment/payment"

async def payment_method_query(
    authorization: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    可用支付方式-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 可用支付方式
    """
    url = f"{base_url}Method/queryPaymentMethodSub"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def store_payment_method(
    authorization: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    门店支付方式-下拉检索用
    #! 与payment_method_query查询内容一致，但此处返回为树状结构，且更详细
    Args:
        authorization (str): 授权token
        tenant_id (int, optional): 租户ID. Defaults to None.
    Returns:
        dict: 门店支付方式
    """
    url = f"{base_url}Group/getStorePaymentMethod"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {}
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def payment_record_index(
    authorization: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    支付状态-下拉检索用
    Args:
        authorization (str): 授权token
        tenant_id (int, optional): 租户ID. Defaults to None.
    Returns:
        dict: 支付状态
    """
    url = f"{base_url}Record/getPaymentRecordIndexEnumVo"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def payment_record_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    query_type: int = 1,
    operationStartTime: Optional[str] = None,
    operationEndTime: Optional[str] = None,
    storeCode: Optional[str] = None,
    orderId: Optional[str] = None,
    documentNumber: Optional[str] = None,
    shopType: Optional[str] = None,
    memberPhone: Optional[str] = None,
    methodCodes: Optional[List[str]] = None,
    status: Optional[int] = None,
    saleType: Optional[int] = None,
    terminalType: Optional[int] = None,
    cashierId: Optional[str] = None,) -> dict:
    """
    零售收款单/退款单查询
    Args:
        authorization (str): 授权token
        tenant_id (int, optional): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        query_type (int): 查询类型 Defaults to 1.
            - 可选值：1-收款单，2-退款单
        operationStartTime (str,None): 操作开始时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        operationEndTime (str,None): 操作结束时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        storeCode (str,None): 门店编码. Defaults to None.
        orderId (str,None): 销售订单号. Defaults to None.
        documentNumber (str,None): 三方单号. Defaults to None.
        shopType (str,None): 店铺类型. Defaults to None.
            - 可选值：1-线下门店，21-O2O-美团，22-O2O-饿了么
        memberPhone (str,None): 会员手机号. Defaults to None.
        methodCodes (List[str],None): 支付方式. Defaults to None.
            - 可在store_payment_method中获取，对应支付方式methodCode字段
        status (int,None): 支付状态. Defaults to None.
            - 可在payment_record_index获取，对应status下的列表
            - 当query_type=1时对应status下的列表
            - 当query_type=2时对应reFundStatus下的列表
        saleType (int,None): 销售类型. Defaults to None.
            - 可在payment_record_index获取，对应saleType下的列表
        terminalType (int,None): 销售终端类型. Defaults to None.
            - 仅在query_type=1时有效
            - 可在payment_record_index获取，对应 terminalType 下的列表
        cashierId (str,None): 收银员id. Defaults to None.
            - 仅在query_type=1时有效
    Returns:
        dict: 零售收款单/退款单查询结果
    """
    url = f"{base_url}Record/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if operationStartTime:
        operation_start_time = get_date_start_and_end_time(operationStartTime)
    else:
        taday = get_current_date()
        operation_start_time = get_date_start_and_end_time(taday)

    if operationEndTime:
        operation_end_time = get_date_start_and_end_time(operationEndTime)
    else:
        operation_end_time = None

    print(f"operation_start_time: {operation_start_time}")
    print(f"operation_end_time: {operation_end_time}")

    payload = {
        "current": current,
        "size": size,
        "type": query_type,
        "operationStartTime": operation_start_time['start_time'] if operation_start_time else None,
        "operationEndTime": operation_end_time['end_time'] if operation_end_time else None,
        "storeCode": storeCode,
        "orderId": orderId,
        "documentNumber": documentNumber,
        "shopType": shopType,
        "memberPhone": memberPhone,
        "methodCodes": methodCodes,
        "status": status,
        "saleType": saleType,
        #! 以下两个参数，尽在query_type=1时有效
        "terminalType": terminalType,
        "cashierId": cashierId,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
