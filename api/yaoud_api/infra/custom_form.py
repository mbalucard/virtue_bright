"""
自定义表单规则
    - 获取字段规则列表-按字段类型: field_rule_list
    - 自定义表单分类-下拉检索用: custom_form_class
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/customForm"


async def field_rule_list(
        authorization: str,
        busClass: str = "GOOD_CLASS",
        tenant_id: Optional[int] = None,
        code: Optional[str] = None,
        systemId: int = 1,
        enterpriseId: Optional[int] = None,) -> dict:
    """
    获取字段规则列表-按字段类型
    Args:
        authorization (str): 认证信息
        busClass (str): 业务类. Defaults to "GOOD_CLASS".
        tenant_id (int, None): 租户ID. Defaults to None.
        code (str, None): 字段编码.
            - 如productType(商品类型)
        systemId (int): 系统ID. 用途未知 Defaults to 1.
        enterpriseId (int, None): 企业ID. Defaults to None.
    Returns:
        dict: 字段规则列表
    """
    url = f"{base_url}Rule/getRuleList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "busClass": busClass,
        "systemId": systemId,
        "enterpriseId": enterpriseId,
        "code": code,
        "tenantId": tenant_id,
        "_t": timestamp()
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def custom_form_class(
        authorization: str,
        tenant_id: Optional[int] = None,
        busClass: str = "SUPPLIER_CLASS") -> dict:
    """
    自定义表单分类-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        busClass (str): 业务类. Defaults to "SUPPLIER_CLASS".
    Returns:
        dict: 自定义表单分类-下拉检索用
    """
    url = f"{base_url}Class/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "busClass": busClass,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
