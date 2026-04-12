"""
发票登记管理
    - 供应商发票登记: supplier_invoice_register
    - 供应商发票登记-详情: supplier_invoice_register_detail
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/cwSupplierInvoiceRegister"


async def supplier_invoice_register(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        orderNo: Optional[str] = None,
        invoiceNumber: Optional[str] = None,
        sourceNo: Optional[str] = None,
        remark: Optional[str] = None,
        supplierIdList: Optional[List[str]] = None,
        supplierDeptIdList: Optional[List[str]] = None,
        createIdList: Optional[List[str]] = None,
        updateIdList: Optional[List[str]] = None,
        orderAttributeList: Optional[List[str]] = None,
        createStartTime: Optional[str] = None,
        createEndTime: Optional[str] = None,
        auditTimeBegin: Optional[str] = None,
        auditTimeEnd: Optional[str] = None,
        updateTimeBegin: Optional[str] = None,
        updateTimeEnd: Optional[str] = None,) -> dict:
    """
    供应商发票登记
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        orderNo (str, None): 发票登记单号. Defaults to None.
        invoiceNumber (str, None): 发票号码. Defaults to None.
        sourceNo (str, None): 关联业务单号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        supplierIdList (List[str], None): 供应商ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取，对应字段id
        supplierDeptIdList (List[str], None): 供应商部门ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取 deptList字段下 
            - 与 supplierIdList 联动
        createIdList (List[str], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        updateIdList (List[str], None): 更新人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        orderAttributeList (List[str], None): 订单属性列表. Defaults to None.
            - 1-正向单据
            - 2-逆向单据
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd HH:mm:ss
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd HH:mm:ss
        auditTimeBegin (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        auditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        updateTimeBegin (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        updateTimeEnd (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    Returns:
        dict: 供应商发票登记
    """
    url = f"{base_url}/list"
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
        "orderNo": orderNo,
        "invoiceNumber": invoiceNumber,
        "sourceNo": sourceNo,
        "remark": remark,
        "supplierIdList": supplierIdList,
        "supplierDeptIdList": supplierDeptIdList if supplierIdList else None,
        "createIdList": createIdList,
        "updateIdList": updateIdList,
        "orderAttributeList": orderAttributeList,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "auditTimeBegin": auditTimeBegin,
        "auditTimeEnd": auditTimeEnd,
        "updateTimeBegin": updateTimeBegin,
        "updateTimeEnd": updateTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()

async def supplier_invoice_register_detail(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    供应商发票登记-详情
    Args:
        authorization (str): 认证信息
        id (str): 单据ID. 
            - 可在 supplier_invoice_register_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商发票登记-详情
    """
    url = f"{base_url}/detail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
    }
    payload = {}
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, params=params, timeout=yaoud_env["timeout"])
    return response.json()

