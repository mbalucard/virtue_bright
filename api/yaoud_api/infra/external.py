"""
外部接口
    - 获取员工列表-下拉检索用: get_employee_list
    - 按角色获取人员信息-下拉检索用: get_employee_list_by_post
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/external"
TTL = yaoud_env["timeout"]


async def get_employee_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,
        current: int = 1,
        size: int = 100,
        enterpriseId: Optional[int] = None,
        organIds: Optional[int] = None,
        postCodes: Optional[List[str]] = None,) -> dict:
    """
    获取员工列表-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (Optional[str], optional): 关键字. Defaults to None.
            - 可搜索员工姓名，手机号，助记码
        current (int, optional): 当前页. Defaults to 1.
        size (int, optional): 每页条目数. Defaults to 100.
        enterpriseId (int, None): 企业ID. Defaults to None.
        postCodes (List[str], None): 角色编码列表.
            - enterpriseId为None时，该字段查询数据无效. Defaults to None.
            - 可在 dict_item_list 中获取,keyword 为岗位
    Returns:
        dict: 员工列表
    """
    url = f"{base_url}/employee/getEmployeeListByPost"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "tenantId": tenant_id,
        "keyword": keyword,
        #! 如果enterpriseId为None，postCodes有值，仅查询租户下有岗位的员工
        "enterpriseId": enterpriseId,
        "organIds": organIds,
        "postCodes": postCodes,  # 可在 employee_organ_post_list 中获取
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def get_employee_list_by_post(
        authorization: str,
        postCode: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    按角色获取人员信息-下拉检索用
    Args:
        authorization (str): 认证信息
        postCode (str): 角色编码
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 
    """
    url = f"{base_url}/employee/getEmployeeListByPost"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "postCode": postCode,  # 可在 employee_organ_post_list 中获取
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
