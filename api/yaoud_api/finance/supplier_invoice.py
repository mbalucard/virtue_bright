"""
发票采集管理
    - 供应商发票列表: supplier_invoice_page
    - 供应商发票采集: supplier_invoice_collection_page
    - 供应商发票采集-详情: supplier_invoice_collection_detail
    - 供应商发票采集-收票记录: supplier_invoice_collection_receive_record
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/supplierInvoice"


async def supplier_invoice_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        invoiceNo: Optional[str] = None,
        invoiceNumber: Optional[str] = None,
        sourceNo: Optional[str] = None,
        remark: Optional[str] = None,
        status: Optional[str] = None,
        supplierIdList: Optional[str] = None,
        supplierDeptIdList: Optional[str] = None,
        invoiceType: Optional[str] = None,
        invoiceAttribute: Optional[str] = None,
        createIds: Optional[str] = None,
        updateIds: Optional[str] = None,
        invoiceAmtStart: Optional[str] = None,
        invoiceAmtEnd: Optional[str] = None,
        faceAmtStart: Optional[str] = None,
        faceAmtEnd: Optional[str] = None,
        noFaceAmtStart: Optional[str] = None,
        noFaceAmtEnd: Optional[str] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        updateStartTime: Optional[str] = None,
        updateEndTime: Optional[str] = None,
        openTimeBegin: Optional[str] = None,
        openTimeEnd: Optional[str] = None,
        finishAuditTimeStart: Optional[str] = None,
        finishAuditTimeEnd: Optional[str] = None,) -> dict:
    """
    供应商发票管理
    #! 无数据，暂未完成测试。
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        invoiceNo (str, None): 单据编号. Defaults to None.
        invoiceNumber (str, None): 发票号码. Defaults to None.
        sourceNo (str, None): 业务单据编号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        status (str, None): 状态. Defaults to None.
            - 0-草稿 1-审批中 2-已完成 4-已作废 3-已驳回
        supplierIdList (str, None): 供应商ID列表. Defaults to None.
            - 多选用逗号隔开
            - 可在 simple_supplier_page 中获取
        supplierDeptIdList (str, None): 供应商部门ID列表. Defaults to None.
            - 多选用逗号隔开
            - 与 supplierIdList 联动
            - 可在 simple_supplier_page 中获取 deptList字段下  
        invoiceType (str, None): 发票类型. Defaults to None.
            - 可在 dict_item_list 中获取，keyword="发票类型",isEnt = 1
        invoiceAttribute (str, None): 发票属性. Defaults to None.
            - 可在 dict_item_list 中获取，keyword="发票属性",isEnt = 1
        createIds (str, None): 创建人ID列表. Defaults to None.
            - 多选用逗号隔开
            - 可在 get_employee_list 中获取
        updateIds (str, None): 更新人ID列表. Defaults to None.
            - 多选用逗号隔开
            - 可在 get_employee_list 中获取
        invoiceAmtStart (str, None): 发票金额区间-最小值. Defaults to None.
        invoiceAmtEnd (str, None): 发票金额区间-最大值. Defaults to None.
        faceAmtStart (str, None): 票面金额区间-最小值. Defaults to None.
        faceAmtEnd (str, None): 票面金额区间-最大值. Defaults to None.
        noFaceAmtStart (str, None): 未到票金额区间-最小值. Defaults to None.
        noFaceAmtEnd (str, None): 未到票金额区间-最大值. Defaults to None.
        createTimeBegin (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        createTimeEnd (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateStartTime (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateEndTime (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        openTimeBegin (str, None): 开票时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        openTimeEnd (str, None): 开票时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        finishAuditTimeStart (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        finishAuditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
    Returns:
        dict: 供应商发票列表
    """
    url = f"{base_url}/pageSum"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createTimeBegin:
        createTimeBegin = get_date_start_and_end_time(createTimeBegin)
    else:
        taday = get_current_date()
        createTimeBegin = get_date_start_and_end_time(taday)
    if createTimeEnd:
        createTimeEnd = get_date_start_and_end_time(createTimeEnd)
    else:
        taday = get_current_date()
        createTimeEnd = get_date_start_and_end_time(taday)
    if updateStartTime:
        updateStartTime = get_date_start_and_end_time(updateStartTime)
    if updateEndTime:
        updateEndTime = get_date_start_and_end_time(updateEndTime)
    if openTimeBegin:
        openTimeBegin = get_date_start_and_end_time(openTimeBegin)
    if openTimeEnd:
        openTimeEnd = get_date_start_and_end_time(openTimeEnd)
    if finishAuditTimeStart:
        finishAuditTimeStart = get_date_start_and_end_time(
            finishAuditTimeStart)
    if finishAuditTimeEnd:
        finishAuditTimeEnd = get_date_start_and_end_time(finishAuditTimeEnd)
    params = {
        "current": current,
        "size": size,
        "invoiceNo": invoiceNo,
        "invoiceNumber": invoiceNumber,
        "sourceNo": sourceNo,
        "remark": remark,
        "status": status,
        "supplierIdList": supplierIdList,
        "supplierDeptIdList": supplierDeptIdList if supplierIdList else None,
        "invoiceType": invoiceType,
        "invoiceAttribute": invoiceAttribute,
        "createIds": createIds,
        "updateIds": updateIds,
        "invoiceAmtStart": invoiceAmtStart,
        "invoiceAmtEnd": invoiceAmtEnd,
        "faceAmtStart": faceAmtStart,
        "faceAmtEnd": faceAmtEnd,
        "noFaceAmtStart": noFaceAmtStart,
        "noFaceAmtEnd": noFaceAmtEnd,
        "createTimeBegin": createTimeBegin['start_time'] if createTimeBegin else None,
        "createTimeEnd": createTimeEnd['end_time'] if createTimeEnd else None,
        "updateStartTime": updateStartTime['start_time'] if updateStartTime else None,
        "updateEndTime": updateEndTime['end_time'] if updateEndTime else None,
        "openTimeBegin": openTimeBegin['start_time'] if openTimeBegin else None,
        "openTimeEnd": openTimeEnd['end_time'] if openTimeEnd else None,
        "finishAuditTimeStart": finishAuditTimeStart['start_time'] if finishAuditTimeStart else None,
        "finishAuditTimeEnd": finishAuditTimeEnd['end_time'] if finishAuditTimeEnd else None,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_invoice_collection_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        invoiceNo: Optional[str] = None,
        invoiceNumber: Optional[str] = None,
        invoiceCode: Optional[str] = None,
        remark: Optional[str] = None,
        orgIdList: Optional[List[str]] = None,
        supplierIdList: Optional[List[str]] = None,
        supplierDeptIdList: Optional[List[str]] = None,
        invoiceTypeList: Optional[List[str]] = None,
        invoiceAttributeList: Optional[List[str]] = None,
        buyTaxList: Optional[List[str]] = None,
        createIdList: Optional[List[str]] = None,
        updateIdList: Optional[List[str]] = None,
        registrationStatusList: Optional[List[str]] = None,
        statusList: Optional[List[str]] = None,
        status: Optional[str] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        receiveStartDate: Optional[str] = None,
        receiveEndDate: Optional[str] = None,
        invoiceStartDate: Optional[str] = None,
        invoiceEndDate: Optional[str] = None,
        updateStartDate: Optional[str] = None,
        updateEndDate: Optional[str] = None,) -> dict:
    """
    供应商发票采集
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        invoiceNo (str, None): 单据编号. Defaults to None.
        invoiceNumber (str, None): 发票号码. Defaults to None.
        invoiceCode (str, None): 发票代码. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        orgIdList (List[str], None): 到票机构ID列表. Defaults to None.
        supplierIdList (List[str], None): 供应商ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取
        supplierDeptIdList (List[str], None): 供应商部门ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取 deptList字段下 
            - 与 supplierIdList 联动
        invoiceTypeList (List[str], None): 发票类型列表. Defaults to None.
            - 可在 dict_item_list 中获取，keyword="发票类型",isEnt = 1
        invoiceAttributeList (List[str], None): 发票属性列表. Defaults to None.
            - 可在 dict_item_list 中获取，keyword="发票属性",isEnt = 1
        buyTaxList (List[str], None): 进项税率列表. Defaults to None.
            - 可在 dict_item_list 中获取，keyword="进项税率"
        createIdList (List[str], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        updateIdList (List[str], None): 更新人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        registrationStatusList (List[str], None): 登记状态列表. Defaults to None.
            - 0-未登记 1-部分登记 2-已登记
        statusList (List[str], None): 单据状态列表. Defaults to None.
            - 0-草稿 1-收票中 2-已退回 3-已作废 4-已完成 5-已关闭
        status (str, None): 单据状态. Defaults to None.
            - 0-草稿 1-收票中 2-已退回 3-已作废 4-已完成 5-已关闭
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        receiveStartDate (str, None): 收票时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        receiveEndDate (str, None): 收票时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        invoiceStartDate (str, None): 开票时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        invoiceEndDate (str, None): 开票时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateStartDate (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd.
        updateEndDate (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd.
    Returns:
        dict: 供应商发票采集
    """
    url = f"{base_url}Collection/pageList"
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

    payload = {
        "current": current,
        "size": size,
        "invoiceNo": invoiceNo,
        "invoiceNumber": invoiceNumber,
        "invoiceCode": invoiceCode,
        "remark": remark,
        "orgIdList": orgIdList,
        "supplierIdList": supplierIdList,
        "supplierDeptIdList": supplierDeptIdList if supplierIdList else None,
        "invoiceTypeList": invoiceTypeList,
        "invoiceAttributeList": invoiceAttributeList,
        "buyTaxList": buyTaxList,
        "createIdList": createIdList,
        "updateIdList": updateIdList,
        "registrationStatusList": registrationStatusList,
        "statusList": statusList,
        "status": status,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "receiveStartDate": receiveStartDate,
        "receiveEndDate": receiveEndDate,
        "invoiceStartDate": invoiceStartDate,
        "invoiceEndDate": invoiceEndDate,
        "updateStartDate": updateStartDate,
        "updateEndDate": updateEndDate,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_invoice_collection_detail(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    供应商发票采集-详情
    Args:
        authorization (str): 认证信息
        id (str): 单据ID. 
            - 可在 supplier_invoice_collection_page 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商发票采集-详情
    """
    url = f"{base_url}Collection/info"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "id": id,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def supplier_invoice_collection_receive_record(
    authorization: str,
    id: str,
    tenant_id: Optional[int] = None,) -> dict:
    """
    供应商发票采集-收票记录
    Args:
        authorization (str): 认证信息
        id (str): 单据ID. 
            - 可在 supplier_invoice_collection_page 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商发票采集-收票记录
    """
    url = f"{base_url}Collection/receiveRecord"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "id": id,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

