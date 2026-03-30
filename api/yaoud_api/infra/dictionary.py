"""
字典管理
    - 字典管理-通用字典: dict_item_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/dict"

async def dict_item_list(
        authorization: str,
        enterpriseId: int,
        keyword: Optional[str] = None,
        tenant_id: Optional[int] = None,
        isEnt: Optional[int] = None,
        chooseOne: Optional[int] = None,) -> dict:
    """
    字典管理-通用字典
    Args:
        authorization (str): 认证信息
        keyword (str, None): 关键字.
            - 支持字段名称，字段编码
        tenant_id (int, None): 租户ID. Defaults to None.
        enterpriseId (int): 企业ID. Defaults to None.
        isEnt (int, None): 是否企业级.Defaults to None.
            - 1-企业字典
            - None-通用字典
        chooseOne (int, None): 包含选项.Defaults to None. 
            - 1-字典分类中包含
            - 2-代码中包含
            - 3-名称中包含
            - 4-备注中包含
    Returns:
        dict: 字典管理-通用字典
    """
    url = f"{base_url}/queryDictItemByKeyword"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    params = {
        "keyword": keyword,
        "enterpriseId": enterpriseId,
        "isEnt": isEnt if enterpriseId else None,
        "chooseOne": chooseOne,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

