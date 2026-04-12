"""
医保字典
    - 医保字典: medical_insurance_dict
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/miaBoss/dictionary"

async def medical_insurance_dict(
        authorization: str,
        tenant_id: Optional[int] = None,
        data_type: Optional[str] = None,) -> dict:
    """
    医保字典
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        data_type (str, None): 数据类别. Defaults to None.
            - med_type-医疗类别
            - clr_type-清除类别
            - psn_cert_type-证件类型
            - insutype-险种类型
            - 参数未收集全
    Returns:
        dict: 医保字典
    """
    url = f"{base_url}/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "type": data_type,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
