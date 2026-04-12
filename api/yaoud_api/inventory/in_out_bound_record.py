"""
出入库
    - 商品出入库流水-按批次: batch_inout_bound
    - 商品出入库流水-按商品: batch_inout_goods
    - 库存业务-业务类型查询-下拉检索用: busines_type
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/inventory/inOutBoundRecord"


async def batch_inout_bound(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        objectType: int = 3,
        inOutNo: Optional[str] = None,
        keyword: Optional[str] = None,
        code: Optional[str] = None,
        barCode: Optional[str] = None,
        batchNo: Optional[str] = None,
        batch: Optional[str] = None,
        oldAllocationCode: Optional[str] = None,
        allocationCode: Optional[str] = None,
        businessNo: Optional[str] = None,
        createName: Optional[str] = None,
        sendWarehouseName: Optional[str] = None,
        receiveWarehouseName: Optional[str] = None,
        inventoryType: Optional[str] = None,
        businessType: Optional[int] = None,
        purchaserId: Optional[str] = None,
        warehouseIds: Optional[List[str]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        total: bool = False,) -> dict:
    """
    商品出入库流水-按批次
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        objectType (int, None): 用途未知. Defaults to 3.
        inOutNo (str, None): 单据号. Defaults to None.
        keyword (str, None): 商品检索. Defaults to None.
            - 支持按商品名称、通用名称、编码、助记码检索
        code (str, None): 商品编码. Defaults to None.
        barCode (str, None): 条形码. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        batch (str, None): 商品批次号. Defaults to None.
        oldAllocationCode (str, None): 旧货位. Defaults to None.
        allocationCode (str, None): 新货位. Defaults to None.
        businessNo (str, None): 关联业务单号. Defaults to None.
            - 必须输入完全
        createName (str, None): 制单人姓名. Defaults to None.
            - 必须全称
        sendWarehouseName (str, None): 出货仓库. Defaults to None.
            - 必须全称
        receiveWarehouseName (str, None): 收货仓库. Defaults to None.
            - 必须全称
        inventoryType (str, None): 单据类型.(1-入库，2-出库) Defaults to None.
            - 1-入库
            - 2-出库
        businessType (int, None): 业务类型. Defaults to None.
            - 仅在 inventoryType 不为 None 时有效, 可在 busines_type 中获取
        purchaserId (str, None): 采购员ID. Defaults to None.
            - 可在 get_employee_list 中获取
        warehouseIds (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        total (bool, None): 是否查询总数. Defaults to False.
            - True: 查询总数
            - False: 查询分页数据
    Returns:
        dict: 商品出入库流水-按批次响应体
    """
    if total:
        url = f"{base_url}/pageByBatchSum"
    else:
        url = f"{base_url}/pageByBatch"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createTimeBegin:
        create_time_begin = get_date_start_and_end_time(createTimeBegin)
    else:
        taday = get_current_date()
        create_time_begin = get_date_start_and_end_time(taday)
    if createTimeEnd:
        create_time_end = get_date_start_and_end_time(createTimeEnd)
    else:
        taday = get_current_date()
        create_time_end = get_date_start_and_end_time(taday)
    payload = {
        "current": current,
        "size": size,
        "objectType": objectType,
        "inOutNo": inOutNo,
        "keyword": keyword,
        "code": code,
        "barCode": barCode,
        "batchNo": batchNo,
        "batch": batch,
        "oldAllocationCode": oldAllocationCode,
        "allocationCode": allocationCode,
        "businessNo": businessNo,
        "createName": createName,
        "sendWarehouseName": sendWarehouseName,
        "receiveWarehouseName": receiveWarehouseName,
        "inventoryType": inventoryType,
        "businessType": businessType if businessType else None,
        "purchaserId": purchaserId,
        "warehouseIds": warehouseIds,
        "createTimeBegin": create_time_begin['start_time'] if create_time_begin else None,
        "createTimeEnd": create_time_end['end_time'] if create_time_end else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def batch_inout_goods(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        objectType: int = 3,
        keyword: Optional[str] = None,
        code: Optional[str] = None,
        barCode: Optional[str] = None,
        inOutNo: Optional[str] = None,
        businessNo: Optional[str] = None,
        createName: Optional[str] = None,
        receiveWarehouseName: Optional[str] = None,
        sendWarehouseName: Optional[str] = None,
        warehouseIds: Optional[List[str]] = None,
        inventoryType: Optional[str] = None,
        businessType: Optional[int] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        total: bool = False,) -> dict:
    """
    商品出入库流水-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页码. Defaults to 1.
        size (int, None): 每页数量. Defaults to 20.
        objectType (int, None): 用途未知. Defaults to 3.
        keyword (str, None): 商品检索. Defaults to None.
            - 支持按商品名称、通用名称、编码、助记码检索
        code (str, None): 商品编码. Defaults to None.
        barCode (str, None): 条形码. Defaults to None.
        inOutNo (str, None): 单据号. Defaults to None.
            - 必须输入完全
        businessNo (str, None): 关联业务单号. Defaults to None.
            - 必须输入完全
        createName (str, None): 制单人姓名. Defaults to None.
            - 必须全称
        receiveWarehouseName (str, None): 收货仓库. Defaults to None.
            - 必须全称
        sendWarehouseName (str, None): 出货仓库. Defaults to None.
            - 必须全称
        warehouseIds (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_warehouse 中获取
        inventoryType (str, None): 单据类型. Defaults to None.
            - 1-入库
            - 2-出库
        businessType (int, None): 业务类型. Defaults to None.
            - 仅在 inventoryType 不为 None 时有效, 可在 busines_type 中获取
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        total (bool, None): 是否查询总数. Defaults to False.
            - True: 查询总数
            - False: 查询分页数据
    Returns:
        dict: 商品出入库流水-按商品响应体
    """
    if total:
        url = f"{base_url}/pageListSum"
    else:
        url = f"{base_url}/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if createTimeBegin:
        create_time_begin = get_date_start_and_end_time(createTimeBegin)
    else:
        taday = get_current_date()
        create_time_begin = get_date_start_and_end_time(taday)
    if createTimeEnd:
        create_time_end = get_date_start_and_end_time(createTimeEnd)
    else:
        create_time_end = None
    payload = {
        "current": current,
        "size": size,
        "objectType": objectType,
        "keyword": keyword,
        "code": code,
        "barCode": barCode,
        "inOutNo": inOutNo,
        "businessNo": businessNo,
        "createName": createName,
        "receiveWarehouseName": receiveWarehouseName,
        "sendWarehouseName": sendWarehouseName,
        "warehouseIds": warehouseIds,
        "inventoryType": inventoryType,
        "businessType": businessType if businessType else None,
        "createTimeBegin": create_time_begin['start_time'] if create_time_begin else None,
        "createTimeEnd": create_time_end['end_time'] if create_time_end else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def busines_type(
        authorization: str,
        inventoryType: int,
        tenant_id: Optional[int] = None,
        objectType: int = 3,) -> dict:
    """
    库存业务-业务类型查询-下拉检索用
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        inventoryType (int): 库存业务类型.
            - 1-入库业务
            - 2-出库业务
        objectType (int, None): 用途未知. Defaults to 3.
    Returns:
        dict: 库存业务-业务类型查询响应体
    """
    url = f"{base_url}/getBusinessType/{inventoryType}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "objectType": objectType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

