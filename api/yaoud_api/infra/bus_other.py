"""
其他类别字典
    - 其他类别字典-下拉检索用: other_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/busOther"


async def other_list(
        authorization: str,
        parentCode: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    其他类别字典-下拉检索用
    #! 在供应商管理发现此接口, 
    Args:
        authorization (str): 认证信息
        parentCode (str): 父级编码. Defaults to None. 
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 其他类别字典-下拉检索用
    """
    url = f"{base_url}/queryOtherList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        # ! 发现对应 business_scope_tree_list 接口中的 businessScopeRefList 返回值，1099
        "parentCode": parentCode,  
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
