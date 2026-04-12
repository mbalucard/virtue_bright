"""
发票
    - 供应商发票列表: supplier_invoice_page
    - 供应商发票采集: supplier_invoice_collection_page
    - 供应商发票采集-详情: supplier_invoice_collection_detail
    - 供应商发票采集-收票记录: supplier_invoice_collection_receive_record
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/documentOperateLog"
TTL = yaoud_env["timeout"]

async def document_operate_log(
        authorization: str,
        docId: str,
        tenant_id: Optional[int] = None,
        docType: int = 305,
        current: int = 1,
        size: int = 20,) -> dict:
    """
    财务单据-操作记录
    Args:
        authorization (str): 认证信息
        docId (str): 单据ID. 
            - 305 可在 supplier_invoice_collection_detail 中获取,对应字段id.
            - 306 可在 supplier_invoice_register_detail 中获取,对应字段id.
        docType (int): 单据类型. Defaults to 305.
            - 305-供应商发票采集
            - 306-供应商发票登记
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
    Returns:
        dict: 财务单据-操作记录
    """
    url = f"{base_url}/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "docType": docType,
        "docId": docId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)

    return response.json()
