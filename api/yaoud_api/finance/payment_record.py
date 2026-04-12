"""
支付记录
    - 支付记录列表: payment_record_list
    - 支付记录详情: payment_record_detail
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/paymentRecord"


async def payment_record_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        paymentNo: Optional[str] = None,
        purchaseOrderNo: Optional[str] = None,
        openingBank: Optional[str] = None,
        bankAccount: Optional[str] = None,
        payTypeList: Optional[List[str]] = None,
        purchaserId: Optional[str] = None,
        createIds: Optional[List[str]] = None,
        updateIds: Optional[List[str]] = None,
        payModeList: Optional[List[str]] = None,
        accountCodeList: Optional[List[str]] = None,
        payMethodList: Optional[List[str]] = None,
        statusList: Optional[List[str]] = None,
        printedStatus: Optional[str] = None,
        transType: str = "4",
        supplierIdList: Optional[List[str]] = None,
        supplierDeptIdList: Optional[List[str]] = None,
        orgType: Optional[str] = None,
        warehouseIdList: Optional[List[str]] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        finishAuditTimeStart: Optional[str] = None,
        finishAuditTimeEnd: Optional[str] = None,
        updateStartTime: Optional[str] = None,
        updateEndTime: Optional[str] = None,
        payDateBegin: Optional[str] = None,
        payDateEnd: Optional[str] = None,) -> dict:
    """
    供应商预付款单/供应商扣款单
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        paymentNo (str, None): 付款单号. Defaults to None.
        purchaseOrderNo (str, None): 采购订单号. Defaults to None.
        openingBank (str, None): 开户行. Defaults to None.
        bankAccount (str, None): 银行账号. Defaults to None.
        payTypeList (List[str], None): 付款类型. Defaults to None.
            -transType=4 时 dict_item_list 中获取，keyword="付款类型",isEnt = 1
            -transType=5 时 dict_item_list 中获取，keyword="扣款类型",isEnt = 1
        purchaserId (str, None): 采购员ID. Defaults to None.
            -可在 get_employee_list 中获取 postCodes=POST_BUYER
        createIds (List[str], None): 创建人ID列表. Defaults to None.
            -可在 get_employee_list 中获取
        updateIds (List[str], None): 更新人ID列表. Defaults to None.
            -可在 get_employee_list 中获取
        payModeList (List[str], None): 付款方式(付款属性). Defaults to None.
            -可在 dict_item_list 中获取，keyword="付款方式",isEnt = 1
        accountCodeList (List[str], None): 结算账户(付款方式). Defaults to None.
            -可在 settlement_account_select_list 中获取
        payMethodList (List[str], None): 付款依据. Defaults to None.
            - 3-按金额 1-按采购订单 2-按金额
        statusList (List[str], None): 单据状态. Defaults to None.
            - 0-草稿 1-审批中 2-已完成 4-已作废 3-已驳回
        printedStatus (str, None): 打印状态. Defaults to None.
            - 0-未打印 1-已打印
        transType (str): 交易类型. Defaults to 4
            - 4-预付款单 5-供应商扣款单 #!其它参数未知
        supplierIdList (List[str], None): 供应商ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取
        supplierDeptIdList (List[str], None): 供应商部门ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取 deptList字段下  与 supplierIdList 联动
        orgType (str, None): 机构类型. Defaults to None.
            - enterprise-企业 warehouse-仓库 store-门店
        warehouseIdList (List[str], None): 付款机构ID. Defaults to None.
            - orgType=warehouse 时 在 synergys_warehouse_info 中获取仓库
            - orgType=enterprise 时，获取企业ID
            - orgType=store 时，在 get_store_list 获取门店ID
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        finishAuditTimeStart (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        finishAuditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateStartTime (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateEndTime (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        payDateBegin (str, None): 付款时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        payDateEnd (str, None): 付款时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
    Returns:
        dict: 供应商预付款单/供应商扣款单
    """
    url = f"{base_url}/pageListPost"
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
    if finishAuditTimeStart:
        finishAuditTimeStart = get_date_start_and_end_time(
            finishAuditTimeStart)
    if finishAuditTimeEnd:
        finishAuditTimeEnd = get_date_start_and_end_time(finishAuditTimeEnd)
    if updateStartTime:
        updateStartTime = get_date_start_and_end_time(updateStartTime)
    if updateEndTime:
        updateEndTime = get_date_start_and_end_time(updateEndTime)
    if payDateBegin:
        payDateBegin = get_date_start_and_end_time(payDateBegin)
    if payDateEnd:
        payDateEnd = get_date_start_and_end_time(payDateEnd)

    payload = {
        "current": current,
        "size": size,
        "paymentNo": paymentNo,
        "purchaseOrderNo": purchaseOrderNo,
        "openingBank": openingBank,
        "bankAccount": bankAccount,
        "payTypeList": payTypeList,
        "purchaserId": purchaserId,
        "createIds": createIds,
        "updateIds": updateIds,
        "payModeList": payModeList,
        "accountCodeList": accountCodeList,
        "payMethodList": payMethodList,
        "statusList": statusList,
        "printedStatus": printedStatus,
        "transType": transType,
        "supplierIdList": supplierIdList,
        "supplierDeptIdList": supplierDeptIdList if supplierIdList else None,
        "orgType": orgType,
        "warehouseIdList": warehouseIdList if orgType else None,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "finishAuditTimeStart": finishAuditTimeStart['start_time'] if finishAuditTimeStart else None,
        "finishAuditTimeEnd": finishAuditTimeEnd['end_time'] if finishAuditTimeEnd else None,
        "updateStartTime": updateStartTime['start_time'] if updateStartTime else None,
        "updateEndTime": updateEndTime['end_time'] if updateEndTime else None,
        "payDateBegin": payDateBegin['start_time'] if payDateBegin else None,
        "payDateEnd": payDateEnd['end_time'] if payDateEnd else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def payment_record_detail(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    供应商预付款单/供应商扣款单-详情
    Args:
        authorization (str): 认证信息
        id (str): 预付款单ID.
            -可在 payment_record_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商预付款单/供应商扣款单-详情
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
