"""
用来存放域名瞎搞的接口
    - 医保清算记录查询-明细: settlement_info_liquidation_detail
    - 每日对账统计: daily_reconciliation_stat
    - 接口参数: interface_parameter
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/mia"


async def settlement_info_liquidation_detail(
        authorization: str,
        orgcodg: str,
        tenant_id: Optional[int] = None,
        setlym: Optional[str] = None,) -> dict:
    """
    医保清算记录查询-明细
    Args:
        authorization (str): 认证信息
        orgcodg (str): 门店医保区化码
            - 可在 settlement_info_liquidation 中获取 orgcodg 字段
        tenant_id (int, None): 租户ID. Defaults to None.
        setlym (str, None): 清算月份. Defaults to None.
            - 格式为: yyyyMM
        Returns:
        dict: 医保清算记录查询-明细
    """
    url = f"{base_url}/liquidation/detail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not setlym:
        taday = get_current_date()
        setlym = int(taday.replace("-", "")[:6])
        # 获取上个月份
        #! 日期不用接口中通用的格式yyyy-MM，我都不说了，调取当月记录还直接报错，按钮致灰，或提示未结算无数据什么的都行，真是一点脑子都没用，植物大战僵尸玩多了吧！
        setlym = str(setlym-1)

    payload = {
        "orgcodg": orgcodg,
        "setlym": setlym,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def daily_reconciliation_stat(
        authorization: str,
        orgcodg: List[str],
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        status: Optional[str] = None,
        stmtDate: Optional[str] = None,
        stmtDateEnd: Optional[str] = None,) -> dict:
    """
    每日对账统计
    Args:
        authorization (str): 认证信息
        orgcodg (list[str]): 门店医保区划码.
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        status (str, None): 对账状态. Defaults to None.
            - 0-对账成功 1-对账失败
        stmtDate (str, None): 日期区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        stmtDateEnd (str, None): 日期区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    """
    url = f"{base_url}/stmtRecordDetail/dailyReconciliationStat"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "orgcodg": orgcodg,
        "status": status,
        "stmtDate": stmtDate if stmtDate else taday,
        "stmtDateEnd": stmtDateEnd if stmtDateEnd else taday,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def interface_parameter(
        authorization: str,
        enterprise_id: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        storeIdList: Optional[List[str]] = None,
        parameterName: Optional[str] = None,
        parameterCode: Optional[str] = None,
        parameterStatus: Optional[str] = None,) -> dict:
    """
    接口参数
    Args:
        authorization (str): 认证信息
        enterprise_id (str): 企业ID
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        storeIdList (list[str], None): 门店ID列表. Defaults to None.
            - 可在 common_organ_of_login_page_of_status 中获取，对应字段id
        parameterName (str, None): 参数名称. Defaults to None.
        parameterCode (str, None): 参数编码. Defaults to None.
        parameterStatus (str, None): 参数状态. Defaults to None.
            - 1-启用 0-禁用

    Returns:
        dict: 接口参数
    """
    url = f"{base_url}/interfaceParameter/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "enterpriseId": enterprise_id,
        "storeIdList": storeIdList,
        "parameterName": parameterName,
        "parameterCode": parameterCode,
        "parameterStatus": parameterStatus,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
