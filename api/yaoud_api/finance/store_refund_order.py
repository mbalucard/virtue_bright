"""
退款
    - 门店回款单列表: store_payment_receipt_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/finance/storeRefundOrder"

async def store_payment_receipt_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    orderNo: Optional[str] = None,
    remark: Optional[str] = None,
    openingBank: Optional[str] = None,
    bankAccount: Optional[str] = None,
    refundBasedList: Optional[List[str]] = None,
    status: Optional[str] = None,
    regionIds: Optional[List[str]] = None,
    storesIdList: Optional[List[str]] = None,
    warehouseIdList: Optional[List[str]] = None,
    storesTypeList: Optional[List[str]] = None,
    refundTypeList: Optional[List[str]] = None,
    refundModeList: Optional[List[str]] = None,
    createIds: Optional[List[str]] = None,
    updateIds: Optional[List[str]] = None,
    createStartTime: Optional[str] = None,
    createEndTime: Optional[str] = None,
    finishAuditTimeStart: Optional[str] = None,
    finishAuditTimeEnd: Optional[str] = None,
    updateStartTime: Optional[str] = None,
    updateEndTime: Optional[str] = None,
    receiveDateBegin: Optional[str] = None,
    receiveDateEnd: Optional[str] = None,)->dict:
    """
    门店回款单列表
    #! 无数据，暂未完成测试。
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条数. Defaults to 20.
        orderNo (str, None): 单据编号. Defaults to None.
        remark (str, None): 备注. Defaults to None.
        openingBank (str, None): 开户行. Defaults to None.
        bankAccount (str, None): 银行账号. Defaults to None.
        refundBasedList (List[str], None): 回款依据列表. Defaults to None.
            - 0-按金额 1-按商品
        status (str, None): 单据状态. Defaults to None.
            - 0-草稿 1-审批中 2-已完成 3-已驳回 4-已作废
        regionIds (List[str], None): 区域ID列表. Defaults to None.
            - 可在 store_region_tree 中获取
        storesIdList (List[str], None): 门店ID列表. Defaults to None.
            - 可在 common_organ_of_login_page_of_status 中获取 id字段
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 synergys_warehouse_info 中获取
        storesTypeList (List[str], None): 门店类型列表. Defaults to None.
            - 可在 dict_item_list 中获取 keyword=门店类型
        refundTypeList (List[str], None): 回款类型列表. Defaults to None.
            - 可在 dict_item_list 中获取 keyword=回款类型 取name 
            - #! 有枚举值不用，用汉字，人才
        refundModeList (List[str], None): 回款方式列表. Defaults to None.
            - 可在 dict_item_list 中获取 keyword=付款方式
        createIds (List[str], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        updateIds (List[str], None): 修改人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        createStartTime (str, None): 制单时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        createEndTime (str, None): 制单时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        finishAuditTimeStart (str, None): 审核时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        finishAuditTimeEnd (str, None): 审核时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        updateStartTime (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        updateEndTime (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        receiveDateBegin (str, None): 回款日期区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        receiveDateEnd (str, None): 回款日期区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    """
    url = f"{base_url}/orderPage"
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
        finishAuditTimeStart = get_date_start_and_end_time(finishAuditTimeStart)
    if finishAuditTimeEnd:
        finishAuditTimeEnd = get_date_start_and_end_time(finishAuditTimeEnd)
    if updateStartTime:
        updateStartTime = get_date_start_and_end_time(updateStartTime)
    if updateEndTime:
        updateEndTime = get_date_start_and_end_time(updateEndTime)

    payload = {
        "current": current,
        "size": size,
        "orderNo": orderNo,
        "remark": remark,
        "openingBank": openingBank,
        "bankAccount": bankAccount,
        "refundBasedList": refundBasedList,
        "status": status,
        "regionIds": regionIds,
        "storesIdList": storesIdList,
        "warehouseIdList": warehouseIdList,
        "storesTypeList": storesTypeList,
        "refundTypeList": refundTypeList,
        "refundModeList": refundModeList,
        "createIds": createIds,
        "updateIds": updateIds,
        "createStartTime": createStartTime['start_time'] if createStartTime else None,
        "createEndTime": createEndTime['end_time'] if createEndTime else None,
        "finishAuditTimeStart": finishAuditTimeStart['start_time'] if finishAuditTimeStart else None,
        "finishAuditTimeEnd": finishAuditTimeEnd['end_time'] if finishAuditTimeEnd else None,
        "updateStartTime": updateStartTime['start_time'] if updateStartTime else None,
        "updateEndTime": updateEndTime['end_time'] if updateEndTime else None,
        "receiveDateBegin": receiveDateBegin,
        "receiveDateEnd": receiveDateEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
