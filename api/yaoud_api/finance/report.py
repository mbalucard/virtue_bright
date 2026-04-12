"""
预付款
    - 订单预付查询: order_prepay_query
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/report"


async def order_prepay_query(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    transNo: Optional[str] = None,
    supplierCode: Optional[str] = None,
    payNo: Optional[str] = None,
    payStartTime: Optional[str] = None,
    payEndTime: Optional[str] = None,
    reportType: str = "supplierPrePayReport",) -> dict:
    """
    订单预付查询
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        transNo (str, None): 订单编号. Defaults to None.
        supplierCode (str, None): 供应商编码. Defaults to None.
            - 可在 supplier_select_list 中获取 code字段
        payNo (str, None): 预付单号. Defaults to None.
            - 仅在 reportType=supplierPrePayDetailReport 或 supplierPrePayDetailReportSum 时有效
        payStartTime (str, None): 付款单日期区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
            - 仅在 reportType=supplierPrePayDetailReport 或 supplierPrePayDetailReportSum 时有效
        payEndTime (str, None): 付款单日期区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
            - 仅在 reportType=supplierPrePayDetailReport 或 supplierPrePayDetailReportSum 时有效
        reportType (str): 查询类型. Defaults to "supplierPrePayReport".
            - supplierPrePayReport-单据 supplierPrePayReportSum-汇总
            - supplierPrePayDetailReport-明细 supplierPrePayDetailReportSum-明细汇总
    Returns:
        dict: 订单预付查询
    """
    url = f"{base_url}/query"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "pageParam": {
            "current": current,
            "size": size,
        },
        "queryParams": {
            "transNo": transNo,
            "supplierCode": supplierCode,

            "payNo": payNo if reportType == "supplierPrePayDetailReport" or reportType == "supplierPrePayDetailReportSum" else None,

            "payStartTime": payStartTime if reportType == "supplierPrePayDetailReport" or reportType == "supplierPrePayDetailReportSum" else None,

            "payEndTime": payEndTime if reportType == "supplierPrePayDetailReport" or reportType == "supplierPrePayDetailReportSum" else None,
        },
        "reportType": reportType,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
