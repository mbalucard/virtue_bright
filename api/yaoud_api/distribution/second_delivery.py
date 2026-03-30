"""
二次配送
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, retrieve_past_date

base_url = f"{yaoud_env['url']}/distribution/secondDelivery"


async def second_delivery_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 10,
    meetType: Optional[int] = None,
    stockoutType: Optional[int] = None,
    storeType: Optional[int] = None,
    businessType: Optional[int] = None,
    secondDeliveryStatus: Optional[int] = None,
    warehouseId: Optional[str] = None,
    goodsIdList: Optional[List[str]] = None,
    storeIdList: Optional[List[str]] = None,
    createIdList: Optional[List[str]] = None,
    businessNo: Optional[str] = None,
    createStartTime: str = retrieve_past_date(7),
    createEndTime: str = get_current_date(),) -> dict:
    """
    二次配送单列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 10.
        meetType (int, None): 订单满座情况. Defaults to None.
            - (0:部分未满足，1:全部未满足)
        stockoutType (int, None): 缺货类型. Defaults to None.
            - (0-商品缺货，1-赠品缺货)
        storeType (int, None): 门店类型. Defaults to None.
            - (1-自营，2-加盟)
        businessType (int, None): 业务类型. Defaults to None.
            - (1-配送)
        secondDeliveryStatus (int, None): 二次配送单状态. Defaults to None.
            - (1-待配送，2-已完成，3-已作废)
        warehouseId (str, None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        storeIdList (List[str], None): 门店ID列表. Defaults to None.
            - 可在 select_stores 中获取
        createIdList (List[str], None): 上次转单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        businessNo (str, None): 业务单号. Defaults to None.
        createStartTime (str): 制单时间区间-开始. Defaults to 7天前.
            - 日期格式为yyyy-MM-dd
        createEndTime (str): 制单时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 二次配送单列表
    """
    url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "meetType": meetType,
        "stockoutType": stockoutType,
        "storeType": storeType,
        "businessType": businessType,
        "secondDeliveryStatus": secondDeliveryStatus,
        "warehouseId": warehouseId,
        "goodsIdList": goodsIdList,
        "storeIdList": storeIdList,
        "createIdList": createIdList,
        "businessNo": businessNo,
        "createStartTime": createStartTime,
        "createEndTime": createEndTime,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()
