"""
供应商对账单
    - 供应商对账单列表: supplier_reconciliation_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/cwSupplierReconciliation"
TTL = yaoud_env["timeout"]


async def supplier_reconciliation_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        orderNo: Optional[str] = None,
        remark: Optional[str] = None,
        orgIdList: Optional[List[str]] = None,
        orderAttributeList: Optional[List[str]] = None,
        orderStatus: Optional[str] = None,
        supplierIdList: Optional[List[str]] = None,
        supplierDeptIdList: Optional[List[str]] = None,
        createIdList: Optional[List[str]] = None,
        updateIdList: Optional[List[str]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        auditTimeBegin: Optional[str] = None,
        auditTimeEnd: Optional[str] = None,
        updateTimeBegin: Optional[str] = None,
        updateTimeEnd: Optional[str] = None,) -> dict:
    """
    供应商对账单列表
    #! 无数据，暂未完成测试。
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        orderNo (str, None): 对账单号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        orgIdList (List[str], None): 结算机构ID列表. Defaults to None.
        orderAttributeList (List[str], None): 单据属性列表. Defaults to None.
            - 1-正向单据 2-负向单据
        orderStatus (str, None): 单据状态. Defaults to None.
            - 0-草稿 1-审批中 2-已完成 3-已驳回 4-已作废
        supplierIdList (List[str], None): 供应商ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取 id字段
        supplierDeptIdList (List[str], None): 供应商部门ID列表. Defaults to None.
            - 可在 simple_supplier_page 中获取 deptList字段下
        createIdList (List[str], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        updateIdList (List[str], None): 修改人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        createTimeBegin (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createTimeEnd (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        auditTimeBegin (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        auditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        updateTimeBegin (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        updateTimeEnd (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    Returns:
        dict: 供应商对账单列表
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    taday = get_current_date()

    payload = {
        "current": current,
        "size": size,
        "orderNo": orderNo,
        "remark": remark,
        "orgIdList": orgIdList,
        "orderAttributeList": orderAttributeList,
        "orderStatus": orderStatus,
        "supplierIdList": supplierIdList,
        "supplierDeptIdList": supplierDeptIdList,
        "createIdList": createIdList,
        "updateIdList": updateIdList,
        "createTimeBegin": createTimeBegin if createTimeBegin else taday,
        "createTimeEnd": createTimeEnd if createTimeEnd else taday,
        "auditTimeBegin": auditTimeBegin,
        "auditTimeEnd": auditTimeEnd,
        "updateTimeBegin": updateTimeBegin,
        "updateTimeEnd": updateTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
