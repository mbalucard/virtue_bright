"""
许可证参数
    - 许可证参数配置-下拉检索用: param_license_cfg
    - 许可证列表: all_license_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/infra/paramLicense"


async def param_license_cfg(
        authorization: str,
        tenant_id: Optional[int] = None,
        size: int = 100,
        goodType: Optional[str] = None,) -> dict:
    """
    许可证参数配置-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        size (int): 每页数量. Defaults to 100.
        goodType (str, None): 许可证类型.
            - 可在 all_license_list 中获取, 对应字段 goodType, 可多选, 用逗号分隔. Defaults to None.
    Returns:
        dict: 许可证参数配置-下拉检索用
    """
    url = f"{base_url}Cfg/getParamLicenseCfg"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "type": 1,
        "size": size,
        "goodType": goodType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

async def all_license_list(
    authorization: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    许可证列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 许可证参数配置
    """
    url = f"{base_url}Cfg/queryAllList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "type": 1,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

