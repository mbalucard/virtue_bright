"""
处方管理
    - 处方签列表: prescription_register_page
    - 处方汇总-按机构或药师汇总: page_stats_prescription
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/oms/prescriptionRegister"


async def prescription_register_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 50,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,
        salesStartTime: Optional[str] = None,
        salesEndTime: Optional[str] = None,
        likeOrderId: Optional[str] = None,
        prescriptionNo: Optional[str] = None,
        name: Optional[str] = None,
        storeId: Optional[str] = None,
        startAge: Optional[int] = None,
        endAge: Optional[int] = None,
        gender: Optional[int] = None,
        status: Optional[int] = None,
        auditName: Optional[str] = None,
        deployName: Optional[str] = None,
        reviewName: Optional[str] = None,) -> dict:
    """
    获取处方签列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 50.
        startTime (str,None): 处方签开始时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        endTime (str,None): 处方签结束时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        salesStartTime (str,None): 销售开始时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        salesEndTime (str,None): 销售结束时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        likeOrderId (str,None): 销售订单号. Defaults to None.
        prescriptionNo (str,None): 处方号. Defaults to None.
        name (str,None): 患者姓名. Defaults to None.
        storeId (str,None): 门店ID. Defaults to None.
        startAge (int,None): 最小年龄. Defaults to None.
        endAge (int,None): 最大年龄. Defaults to None.
        gender (int,None): 性别. Defaults to None.
        status (int,None): 处方状态. Defaults to None.
        auditName (str,None): 审方要事. Defaults to None.
        deployName (str,None): 调配人员. Defaults to None.
        reviewName (str,None): 复核人员. Defaults to None.
    Returns:
        dict: 处方签列表
    """
    url = f"{base_url}/getElectronPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startTime:
        start_time = get_date_start_and_end_time(startTime)
    else:
        taday = get_current_date()
        start_time = get_date_start_and_end_time(taday)
    if endTime:
        end_time = get_date_start_and_end_time(endTime)
    else:
        end_time = None
    if salesStartTime:
        sales_start_time = get_date_start_and_end_time(salesStartTime)
    else:
        sales_start_time = None
    if salesEndTime:
        sales_end_time = get_date_start_and_end_time(salesEndTime)
    else:
        sales_end_time = None


    payload = {
        "current": current,
        "size": size,
        "startTime": start_time['start_time'] if start_time else None,
        "endTime": end_time['end_time'] if end_time else None,
        "salesStartTime": sales_start_time['start_time'] if sales_start_time else None,
        "salesEndTime": sales_end_time['end_time'] if sales_end_time else None,
        "likeOrderId": likeOrderId,
        "prescriptionNo": prescriptionNo,
        "name": name,
        "storeId": storeId,
        "startAge": startAge,
        "endAge": endAge,
        "gender": gender,
        "status": status,
        "auditName": auditName,
        "deployName": deployName,
        "reviewName": reviewName,
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()




async def page_stats_prescription(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    groupByType: Optional[int] = None,
    startTime: Optional[str] = None,
    endTime: Optional[str] = get_current_date(),
    sfFlag: Optional[str] = None,
    storeIds: Optional[List[str]] = None,
    startAuditNum: Optional[int] = None,
    endAuditNum: Optional[int] = None,
    startaverageNum: Optional[int] = None,
    endaverageNum: Optional[int] = None,
    startApprovedNum: Optional[int] = None,
    endApprovedNum: Optional[int] = None,
    startRefuseNum: Optional[int] = None,
    endRefuseNum: Optional[int] = None,
    startPrescriptionNum: Optional[int] = None,
    endPrescriptionNum: Optional[int] = None,
    auditIdList: Optional[List[str]] = None,) -> dict:
    """
    获取处方汇总-按机构或药师汇总
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        groupByType (int, None): 汇总类型. Defaults to None.
            - 可选值：None-门店处方汇总，1-药师处方汇总
        startTime (str, None): 开始时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        endTime (str, None): 结束时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        sfFlag (str, None): 审方类型. Defaults to None.
            - 可选值：1-远程审方，0-本地审方
        storeIds (List[str], None): 门店ID列表. Defaults to None.
        startAuditNum (int, None): 审核总处方量区间-最小值. Defaults to None.
        endAuditNum (int, None): 审核总处方量区间-最大值. Defaults to None.
        startaverageNum (int, None): 每日平均处方量区间-最小值. Defaults to None.
        endaverageNum (int, None): 每日平均处方量区间-最大值. Defaults to None.
        startApprovedNum (int, None): 审核通过处方量区间-最小值. Defaults to None.
        endApprovedNum (int, None): 审核通过处方量区间-最大值. Defaults to None.
        startRefuseNum (int, None): 审核驳回量区间-最小值. Defaults to None.
        endRefuseNum (int, None): 审核驳回量区间-最大值. Defaults to None.
        startPrescriptionNum (int, None): 处方总量区间-最小值. Defaults to None.
            - 当groupByType=None时，该字段有效
        endPrescriptionNum (int, None): 处方总量区间-最大值. Defaults to None.
            - 当groupByType=None时，该字段有效
        auditIdList (List[str], None): 药师ID列表. Defaults to None.
            - 当groupByType=1时，该字段有效
    Returns:
        dict: 处方汇总
    """
    url = f"{base_url}/pageStatsPrescription"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startTime:
        startTime = get_date_start_and_end_time(startTime)
    if endTime:
        endTime = get_date_start_and_end_time(endTime)

    taday = get_current_date()
    taday_time = get_date_start_and_end_time(taday)

    payload = {
        "current": current,
        "size": size,
        "groupByType": groupByType,
        "startTime": startTime['start_time'] if startTime else taday_time['start_time'],
        "endTime": endTime['end_time'] if endTime else taday_time['end_time'],
        "sfFlag": sfFlag,
        "storeIds": storeIds,
        "startAuditNum": startAuditNum,
        "endAuditNum": endAuditNum,
        "startaverageNum": startaverageNum,
        "endaverageNum": endaverageNum,
        "startApprovedNum": startApprovedNum,
        "endApprovedNum": endApprovedNum,
        "startRefuseNum": startRefuseNum,
        "endRefuseNum": endRefuseNum,
        "startPrescriptionNum": startPrescriptionNum,
        "endPrescriptionNum": endPrescriptionNum,
        # 可在get_employee_list中获取，enterpriseId不能为None,postCodes="POST_PHARMACIST"
        "auditIdList": auditIdList,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
    