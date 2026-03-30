"""
门店开票
    - 门店开票单列表: store_invoice_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/cwStoreInvoice"


async def store_invoice_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    orderNo: Optional[str] = None,
    invoiceNo: Optional[str] = None,
    orderRemark: Optional[str] = None,
    invoiceStatus: Optional[str] = None,
    invoiceMethodList: Optional[List[str]] = None,
    invoicePathList: Optional[List[str]] = None,
    pushTypeList: Optional[List[str]] = None,
    amtMin: Optional[float | int] = None,
    amtMax: Optional[float | int] = None,
    invoiceAttributeList: Optional[List[str]] = None,
    invoiceTypeList: Optional[List[str]] = None,
    productIdList: Optional[List[str]] = None,
    createStartTime: Optional[str] = None,
    createEndTime: Optional[str] = None,
    auditTimeBegin: Optional[str] = None,
    auditTimeEnd: Optional[str] = None,
    updateTimeBegin: Optional[str] = None,
    updateTimeEnd: Optional[str] = None,)->dict:
    """
    门店开票单列表
    #! 无数据，暂未完成测试。
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        orderNo (str, None): 单据编号. Defaults to None.
        invoiceNo (str, None): 发票号. Defaults to None.
        orderRemark (str, None): 备注. Defaults to None.
        invoiceStatus (str, None): 单据状态. Defaults to None.
            - 0-草稿 1-审批中 2-开票中 6-开票失败 4-已作废 5-已关闭 3-已驳回 8-已失败 7-已完成 9-冲红中 10-已冲红 11-冲红失败.
        invoiceMethodList (List[str], None): 开票方式列表. Defaults to None.
            - by_details-按明细开票 by_document-按订单开票.
        invoicePathList (List[str], None): 开票路径列表. Defaults to None.
            - 1-人工开票  2-自动开票  3-药同步开票.
        pushTypeList (List[str], None): 推送方式列表. Defaults to None.
            - mobilephone-手机推送 email-邮箱推送 nopush-不推送.
        amtMin (float | int, None): 金额区间-最小. Defaults to None.
        amtMax (float | int, None): 金额区间-最大. Defaults to None.
        invoiceAttributeList (List[str], None): 发票属性列表. Defaults to None.
            - 可在 dict_item_list 中获取 keywork="发票属性".
        invoiceTypeList (List[str], None): 发票类型列表. Defaults to None.
            - 可在 dict_item_list 中获取 keywork="发票类型".
        productIdList (List[str], None): 商品ID列表. Defaults to None.
            - 可在 goods_page_list 中获取.
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        auditTimeBegin (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        auditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateTimeBegin (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateTimeEnd (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.

        #! 以下为缺失字段
            - 门店 疑似从 enterprise_detail 中获取
            - 开票人 收款人 复合人 制单人 修改人 疑似从 get_employee_list 中获取
            - 修改时间 疑似格式:yyyy-MM-dd HH:mm:ss
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createStartTime:
        createStartTime = get_date_start_and_end_time(createStartTime)
    else:
        taday = get_current_date()
        createStartTime = get_date_start_and_end_time(taday)
    if createEndTime:
        createEndTime = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        createEndTime = get_date_start_and_end_time(taday)
    payload = {
        "current": current,
        "size": size,
        "orderNo": orderNo,
        "invoiceNo": invoiceNo,
        "orderRemark": orderRemark,
        "invoiceStatus": invoiceStatus,
        "invoiceMethodList": invoiceMethodList,
        "invoicePathList": invoicePathList,
        "pushTypeList": pushTypeList,
        "amtMin": amtMin,
        "amtMax": amtMax,
        "invoiceAttributeList": invoiceAttributeList,
        "invoiceTypeList": invoiceTypeList,
        "productIdList": productIdList,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "auditTimeBegin": auditTimeBegin,
        "auditTimeEnd": auditTimeEnd,
        "updateTimeBegin": updateTimeBegin,
        "updateTimeEnd": updateTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
