"""
调价审核
    - 零售价格组-调价记录-审批信息详情: price_record_adjust_audit
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/shopProduct/adjustAudit"


async def price_record_adjust_audit(
        authorization: str,
        priceRecordId: int | str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    零售价格组-调价记录-审批信息详情
    Args:
        authorization (str): 认证信息
        priceRecordId (int | str): 调价记录ID. Defaults to None.
            - 可在 price_record_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 零售价格组-调价记录-审批信息详情
    """
    url = f"{base_url}/selectByPriceRecordId"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "priceRecordId": priceRecordId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
