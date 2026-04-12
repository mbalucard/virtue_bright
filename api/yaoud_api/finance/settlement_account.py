"""
结算账户
    - 结算账户列表: settlement_account_list
    - 结算账户详情: settlement_account_detail
    - 结算账户-下拉检索: settlement_account_select_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/cwSettlementAccount"


async def settlement_account_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        accountCode: Optional[str] = None,
        accountName: Optional[str] = None,
        openingBank: Optional[str] = None,
        bankAccount: Optional[str] = None,
        remark: Optional[str] = None,
        createIdList: Optional[List[str]] = None,
        updateIdList: Optional[List[str]] = None,
        payMode: Optional[List[str]] = None,
        accountEnable: Optional[int] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        updateTimeBegin: Optional[str] = None,
        updateTimeEnd: Optional[str] = None,) -> dict:
    """
    结算账户列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 每页条数. Defaults to 20.
        accountCode (str, None): 结算账户编码. Defaults to None.
        accountName (str, None): 结算账户名称. Defaults to None.
        openingBank (str, None): 开户行. Defaults to None.
        bankAccount (str, None): 银行账号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        createIdList (List[str], None): 创建人ID列表.Defaults to None.
            -可在 get_employee_list 中获取
        updateIdList (List[str], None): 更新人ID列表.Defaults to None.
            -可在 get_employee_list 中获取
        payMode (List[str], None): 支付方式.Defaults to None.
            -可在 dict_item_list 中获取，keyword="支付方式",isEnt = 1
        accountEnable (int, None): 结算账户状态. 1-启用 0-禁用. Defaults to None.
        createTimeBegin (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        createTimeEnd (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateTimeBegin (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateTimeEnd (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
    Returns:
        dict: 结算账户列表
    """
    url = f"{base_url}/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "accountCode": accountCode,
        "accountName": accountName,
        "openingBank": openingBank,
        "bankAccount": bankAccount,
        "remark": remark,
        "createIdList": createIdList,
        "updateIdList": updateIdList,
        "payMode": payMode,
        "accountEnable": accountEnable,
        "createTimeBegin": createTimeBegin,
        "createTimeEnd": createTimeEnd,
        "updateTimeBegin": updateTimeBegin,
        "updateTimeEnd": updateTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def settlement_account_detail(
        authorization: str,
        id: int,
        tenant_id: Optional[int] = None,) -> dict:
    """
    结算账户详情
    Args:
        authorization (str): 认证信息
        id (int): 结算账户ID.Defaults to None.
            -可在 settlement_account_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 结算账户详情
    """
    url = f"{base_url}/detail"
    headers = {
        "Authorization": authorization,
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


async def settlement_account_select_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    结算账户-下拉检索
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str, None): 关键字. Defaults to None.
            #! 目前没发现能搜索啥
    Returns:
        dict: 结算账户-下拉检索结果
    """
    url = f"{base_url}/selectList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "keyword": keyword,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

