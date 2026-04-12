"""
结算
    - 结算单列表: settlement_page_list
    - 结算单详情: settlement_info_detail
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/settlement"


async def settlement_page_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        statusList: Optional[List[str]] = None,
        settlementNo: Optional[str] = None,
        orgType: Optional[str] = None,
        warehouseIdList: Optional[str] = None,
        supplierIdList: Optional[str] = None,
        supplierDeptIdList: Optional[str] = None,
        payModeList: Optional[List[str]] = None,
        createIds: Optional[str] = None,
        updateIds: Optional[str] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        writeOffStartDate: Optional[str] = None,
        writeOffEndDate: Optional[str] = None,
        finishAuditTimeStart: Optional[str] = None,
        finishAuditTimeEnd: Optional[str] = None,
        updateStartTime: Optional[str] = None,
        updateEndTime: Optional[str] = None,) -> dict:
    """
    供应商结算单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        statusList (List[str], None): 结算单状态列表. Defaults to None.
            - 0-草稿 1-审批中 2-已完成 4-已作废 3-已驳回
        settlementNo (str, None): 结算单号. Defaults to None.
        #! 下面这些多选需要用逗号隔开的，你他妈的不认识英文啊，字段名都叫list了，你还搞成全字符串，你他妈的脑子里装的是屎吗？ 而且这里面的多选多数都是几百个选项，你他妈用get方式，不是找报错。
        orgType (str, None): 机构类型. Defaults to None.
            - enterprise-企业 warehouse-仓库 store-门店
        warehouseIdList (str, None): 结算机构ID. Defaults to None.
            - 多选用逗号隔开
            - orgType=warehouse 时 在 synergys_warehouse_info 中获取仓库
            - orgType=enterprise 时，获取企业ID
            - orgType=store 时，在 get_store_list 获取门店ID
        supplierIdList (str, None): 供应商ID列表. Defaults to None.
            - 多选用逗号隔开
            - 可在 simple_supplier_page 中获取
        supplierDeptIdList (str, None): 供应商部门ID列表. Defaults to None.
            - 多选用逗号隔开
            - 与 supplierIdList 联动
            - 可在 simple_supplier_page 中获取 deptList字段下  
        payModeList (List[str], None): 付款方式(付款属性). Defaults to None.
            - 可在 dict_item_list 中获取，keyword="付款方式",isEnt = 1
        createIds (str, None): 创建人ID列表. Defaults to None.
            - 多选用逗号隔开
            - 可在 get_employee_list 中获取
        updateIds (str, None): 更新人ID列表. Defaults to None.
            - 多选用逗号隔开
            - 可在 get_employee_list 中获取
        createStartTime (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        createEndTime (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        writeOffStartDate (str, None): 结算时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        writeOffEndDate (str, None): 结算时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        finishAuditTimeStart (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        finishAuditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateStartTime (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateEndTime (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
    Returns:
        dict: 供应商结算单列表
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createStartTime:
        createStartTime = get_date_start_and_end_time(createStartTime)
    else:
        taday = get_current_date()
        createStartTime = get_date_start_and_end_time(taday)
    if createEndTime:
        createEndTime = get_date_start_and_end_time(createEndTime)
    else:
        taday = get_current_date()
        createEndTime = get_date_start_and_end_time(taday)
    if writeOffStartDate:
        writeOffStartDate = get_date_start_and_end_time(writeOffStartDate)
    if writeOffEndDate:
        writeOffEndDate = get_date_start_and_end_time(writeOffEndDate)
    params = {
        "current": current,
        "size": size,
        "statusList": statusList,
        "settlementNo": settlementNo,
        "orgType": orgType,
        "warehouseIdList": warehouseIdList if orgType else None,
        "supplierIdList": supplierIdList,
        "supplierDeptIdList": supplierDeptIdList if supplierIdList else None,
        "payModeList": payModeList,
        "createIds": createIds,
        "updateIds": updateIds,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "writeOffStartDate": writeOffStartDate['start_time'] if writeOffStartDate else None,
        "writeOffEndDate": writeOffEndDate['end_time'] if writeOffEndDate else None,
        "_t": timestamp(),
    }
    # 处理时间区间为None时，报错的问题
    if finishAuditTimeStart:
        finishAuditTimeStart = get_date_start_and_end_time(
            finishAuditTimeStart)
        params["finishAuditTimeStart"] = finishAuditTimeStart['start_time']
    if finishAuditTimeEnd:
        finishAuditTimeEnd = get_date_start_and_end_time(finishAuditTimeEnd)
        params["finishAuditTimeEnd"] = finishAuditTimeEnd['end_time']
    if updateStartTime:
        updateStartTime = get_date_start_and_end_time(updateStartTime)
        params["updateStartTime"] = updateStartTime['start_time']
    if updateEndTime:
        updateEndTime = get_date_start_and_end_time(updateEndTime)
        params["updateEndTime"] = updateEndTime['end_time']

    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def settlement_info_detail(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    供应商结算单-详情
    Args:
        authorization (str): 认证信息
        id (str): 结算单ID.
            -可在 settlement_page_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商结算单-详情
    """
    url = f"{base_url}/info"
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
