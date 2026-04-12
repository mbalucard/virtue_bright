"""
退仓
    - 退仓单-按单据: return_to_warehouse
    - 退仓单-按商品: return_goodes_to_warehouse
    - 退仓单-单据明细: return_to_warehouse_detail
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, retrieve_past_date

base_url = f"{yaoud_env['url']}/distribution/goods"


async def return_to_warehouse(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    withdrawalTypes: Optional[List[int]] = None,
    field: Optional[str] = "createTime",
    order: Optional[str] = "desc",
    tabStatus: int = 0,
    associationApplyNo: Optional[str] = None,
    warehouseId: Optional[str] = None,
    stoId: Optional[int] = None,
    createId: Optional[str] = None,
    createStartTime: str = get_current_date(),
    createEndTime: str = get_current_date(),
    remark: Optional[str] = None,
    submitId: Optional[str] = None,
    withdrawalNo: Optional[str] = None,
    submitStartTime: Optional[str] = None,
    submitEndTime: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    退仓单-按单据
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        withdrawalTypes (List[int], None): 单据类型,. Defaults to None.
            - (1-主动退仓单,2-退仓申请单,3-期初退仓单,4-调拨退仓单,5-直配退仓单,6-药诊退仓单,7-COP退仓单,8-委托退仓单,9-B2C退仓单,10-代储代运退仓单)
        field (str, optional): 排序字段. Defaults to "createTime".
            - createTime表示制单时间
        order (str, optional): 排序方向. Defaults to "desc".
            - desc表示降序，asc表示升序
        tabStatus (int): 单据状态. Defaults to 0.
            - (0-全部，1-草稿，2-审批中，3-待门店出库，8-待仓库入库，4-已完成，5-已作废，6-已关闭，7-已驳回)
        associationApplyNo (str, None): 关联单号. Defaults to None.
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取
        stoId (int, None): 门店ID. Defaults to None.
            - 可在 select_stores 中获取
        createId (str, None): 制单人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        createStartTime (str, None): 制单时间区间-开始. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        remark (str, None): 整单备注. Defaults to None.
        #! 以下参数为空时，不可在提交信息中出现，否则会报服务器异常。
        submitId (str, None): 提交人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        withdrawalNo (str, None): 退仓单号. Defaults to None.
        submitStartTime (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitEndTime (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 退仓单-按单据
    """
    url = f"{base_url}/withdrawal/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "withdrawalTypes": withdrawalTypes,
        "field": field,
        "order": order,
        "tabStatus": tabStatus,
        "associationApplyNo": associationApplyNo,
        "warehouseId": warehouseId,
        "stoId": stoId,
        "createId": createId,
        "createStartTime": createStartTime,
        "createEndTime": createEndTime,
        "remark": remark,
        "_t": timestamp(),
    }
    if submitId:
        params["submitId"] = submitId
    if withdrawalNo:
        params["withdrawalNo"] = withdrawalNo
    if submitStartTime:
        params["submitStartTime"] = submitStartTime
    if submitEndTime:
        params["submitEndTime"] = submitEndTime
    if takeEffectTimeStart:
        params["takeEffectTimeStart"] = takeEffectTimeStart
    if takeEffectTimeEnd:
        params["takeEffectTimeEnd"] = takeEffectTimeEnd
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def return_goodes_to_warehouse(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 10,
        field: Optional[str] = "createTime",
        order: Optional[str] = "desc",
        tabStatus: int = 0,
        withdrawalTypes: Optional[List[int]] = None,
        warehouseId: Optional[str] = None,
        stoId: Optional[int] = None,
        associationApplyNo: Optional[str] = None,
        remark: Optional[str] = None,
        createStartTime: str = get_current_date(),
        createEndTime: str = get_current_date(),
        materialsList: Optional[List[str]] = None,
        withdrawalNo: Optional[str] = None,
        submitStartTime: Optional[str] = None,
        submitEndTime: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    退仓单-按商品
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        field (str, optional): 排序字段. Defaults to "createTime".
            - createTime表示制单时间
        order (str, optional): 排序方向. Defaults to "desc".
            - desc表示降序，asc表示升序
        tabStatus (int): 单据状态，. Defaults to 0.
            - (0-全部，1-草稿，2-审批中，3-待门店出库，8-待仓库入库，4-已完成，5-已作废，6-已关闭，7-已驳回)
        withdrawalTypes (List[int], None): 单据类型. Defaults to None.
            - (1-主动退仓单,2-退仓申请单,3-期初退仓单,4-调拨退仓单,5-直配退仓单,6-药诊退仓单,7-COP退仓单,8-委托退仓单,9-B2C退仓单,10-代储代运退仓单)
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取
        stoId (int, None): 门店ID. Defaults to None.
            - 可在 select_stores 中获取
        associationApplyNo (str, None): 关联单号. Defaults to None.
        remark (str, None): 整单备注. Defaults to None.
        createStartTime (str, None): 制单时间区间-开始. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        #! 以下参数为空时，不可在提交信息中出现，否则会报服务器异常。
        materialsList (List[str], None): 商品编码列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        withdrawalNo (str, None): 退仓单号. Defaults to None.
        submitStartTime (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitEndTime (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 退仓单-按商品
    """
    url = f"{base_url}/withdrawal/detailPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "field": field,
        "order": order,
        "tabStatus": tabStatus,
        "withdrawalTypes": withdrawalTypes,
        "warehouseId": warehouseId,
        "stoId": stoId,
        "associationApplyNo": associationApplyNo,
        "remark": remark,
        "createStartTime": createStartTime,
        "createEndTime": createEndTime,
        "_t": timestamp(),
    }
    if materialsList:
        params["materialsList"] = materialsList
    if withdrawalNo:
        params["withdrawalNo"] = withdrawalNo
    if submitStartTime:
        params["submitStartTime"] = submitStartTime
    if submitEndTime:
        params["submitEndTime"] = submitEndTime
    if takeEffectTimeStart:
        params["takeEffectTimeStart"] = takeEffectTimeStart
    if takeEffectTimeEnd:
        params["takeEffectTimeEnd"] = takeEffectTimeEnd
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def return_to_warehouse_detail(
        authorization: str,
        return_to_warehouse_id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    退仓单-单据明细
    Args:
        authorization (str): 认证信息
        return_to_warehouse_id (str): 退仓单ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 退仓单-单据明细
    """
    url = f"{base_url}/withdrawal/getDetail/{return_to_warehouse_id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
