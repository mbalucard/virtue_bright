"""
发票审核记录
    - 供应商发票登记-审核记录: audit_record
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/cwAuditRecord"
TTL = yaoud_env["timeout"]


async def audit_record(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,
        type: int = 2,) -> dict:
    """
    供应商发票登记-审核记录
    Args:
        authorization (str): 认证信息
        id (str): 单据ID. 
            - 可在 supplier_invoice_register_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
        type (int): 审核类型. Defaults to 2.
            - #! 用途未知
    Returns:
        dict: 供应商发票登记-审核记录
    """
    url = f"{base_url}/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "objectId": id,
        "type": type,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
