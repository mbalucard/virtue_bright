"""
会员分级
    - 会员组分级列表-下拉菜单检索: get_grade_by_group_id
    - 会员等级列表: member_grade_list
    - 会员等级详情: member_grade_detail
"""


from httpx import AsyncClient
from typing import Optional

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time,timestamp


base_url = f"{yaoud_env['url']}/cdp/grade"

async def get_grade_by_group_id(
        authorization: str,
        groupId: int,
        tenant_id: Optional[int] = None,
        member_type: Optional[str] = "free_member",
        requestSource: Optional[str] = "web",) -> dict:
    """
    会员组分级列表-下拉菜单检索
    Args:
        authorization (str): 认证信息
        groupId (int): 会员权益组id
            - 可在 get_member_group_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
        member_type (str, None): 会员组类型. Defaults to "free_member".
        requestSource (str, None): 请求来源. Defaults to "web".
    Returns:
        dict: 会员组分级列表
    """
    url = f"{base_url}/getGradeByGroupId"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "groupId": groupId,
        "type": member_type,
        "requestSource": requestSource,
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def member_grade_list(
    authorization: str,
    groupId: str,
    gradeType: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    会员等级列表
    Args:
        authorization (str): 认证信息
        groupId (str): 会员权益组ID. 
            -可在 get_member_group_list 中获取.
        gradeType (str): 会员等级类型. 
            -可在 member_grade_type 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员等级列表
    """
    url = f"{base_url}/list"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "groupId": groupId,
        "gradeType": gradeType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def member_grade_detail(
    authorization: str,
    id: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    会员等级详情
    Args:
        authorization (str): 认证信息
        id (str): 会员等级ID. 
            -可在 member_grade_list 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员等级详情
    """
    url = f"{base_url}/details"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json() 

    