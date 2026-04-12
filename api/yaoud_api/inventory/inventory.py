"""
盘点管理
    - 盘点-盘点计划: inventory_plan_list
    - 盘点-盘点单-按整单: inventory_taking_list
    - 盘点-盘点单-按商品: inventory_taking_dtl_list
    - 盘点-盈亏单、库存调整记录: inventory_profit_loss_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/inventory/inventory"
TTL = yaoud_env["timeout"]

async def inventory_plan_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        documentNoLike: Optional[str] = None,
        inventoryType: Optional[int] = None,
        createIdList: Optional[List[str]] = None,
        warehouseIdList: Optional[List[str]] = None,
        statusList: Optional[List[str]] = None,
        regionIdList: Optional[List[str]] = None,
        createDateStartStr: Optional[str] = None,
        createDateEndStr: Optional[str] = None,
        takeEffectTimeStart: Optional[str] = None,
        takeEffectTimeEnd: Optional[str] = None,) -> dict:
    """
    盘点-盘点计划
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNoLike (str, None): 单据号. Defaults to None.
        inventoryType (int, None): 盘点类型. Defaults to None.
            - 可选值：1-抽盘，2-全盘，3-随机盘，5-动销盘，6-中药盘，7-非中药盘，8-柜组盘，9-品类盘
        createIdList (List[str], None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_store_warehouse(门店仓库) 与 select_warehouse(仓库) 中获取
        statusList (List[str], None): 状态列表. Defaults to None.
            - 可选值：DRAFT-草稿,SUBMITTED-审批中，CORRECTION-库存调整中，CORRECTION_FAIL-库存调整失败，COMPLETED-盘点完成，TURN-已驳回，CANCEL-已作废，["TOINVENTORY", "INVENTORYTAKING"]-盘点中
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - 可在 store_region_tree 中获取
        createDateStartStr (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createDateEndStr (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str, None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str, None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 盘点-盘点计划响应体
    """
    url = f"{base_url}Plan/selectPageInfo"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "objectType": 3,
        "documentNoLike": documentNoLike,
        "inventoryType": inventoryType,
        "createIdList": createIdList,
        "warehouseIdList": warehouseIdList,
        "statusList": statusList,
        "regionIdList": regionIdList,
        "createDateStartStr": createDateStartStr if createDateStartStr else taday,
        "createDateEndStr": createDateEndStr if createDateEndStr else taday,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def inventory_taking_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        documentNoLike: Optional[str] = None,
        planNo: Optional[str] = None,
        createName: Optional[str] = None,
        submitName: Optional[str] = None,
        inventoryType: Optional[int] = None,
        genProfitLoss: Optional[int] = None,
        statusList: Optional[List[str]] = None,
        warehouseIdList: Optional[List[str]] = None,
        regionIdList: Optional[List[str]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        submitTimeBegin: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,) -> dict:
    """
    盘点-盘点单-按整单
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNoLike (str, None): 单据号. Defaults to None.
        planNo (str, None): 盘点计划单号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        submitName (str, None): 提交人. Defaults to None.
        inventoryType (int, None): 盘点类型. Defaults to None.
            - 可选值：1-抽盘，2-全盘，3-随机盘，5-动销盘，6-中药盘，7-非中药盘，8-柜组盘，9-品类盘
        genProfitLoss (int, None): 生成盈亏单. 可选值：1-是，0-否. Defaults to None.
        statusList (List[str], None): 盘点状态. Defaults to None.
            - 可选值：["INVENTORYTAKING"," INVENTORIED"]-盘点中，["COMPLETED"]-盘点完成,["CANCEL"]-已作废
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_store_warehouse(门店仓库) 与 select_warehouse(仓库) 中获取
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - 可在 store_region_tree 中获取
        createTimeBegin (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeBegin (str, None): 提交时间区间-开始. Defaults to None.
        submitTimeEnd (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 盘点-盘点单-按整单响应体
    """

    url = f"{base_url}Taking/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "objectType": 3,
        "documentNo": documentNoLike,
        "planNo": planNo,
        "createName": createName,
        "submitName": submitName,
        "inventoryType": inventoryType,
        "genProfitLoss": genProfitLoss,
        "statusList": statusList,
        "warehouseIdList": warehouseIdList,
        "regionIdList": regionIdList,
        "createTimeBegin": createTimeBegin if createTimeBegin else taday,
        "createTimeEnd": createTimeEnd if createTimeEnd else taday,
        "submitTimeBegin": submitTimeBegin,
        "submitTimeEnd": submitTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()

async def inventory_taking_dtl_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        documentNo: Optional[str] = None,
        planNo: Optional[str] = None,
        createName: Optional[str] = None,
        submitName: Optional[str] = None,
        batchNo: Optional[str] = None,
        inventoryType: Optional[int] = None,
        statusList: Optional[List[str]] = None,
        genProfitLoss: Optional[int] = None,
        allocationTypes: Optional[List[str]] = None,
        warehouseIdList: Optional[List[str]] = None,
        areaIds: Optional[List[str]] = None,
        cabinetIds: Optional[List[str]] = None,
        goodsIdList: Optional[List[str]] = None,
        allocationIds: Optional[List[str]] = None,
        regionIdList: Optional[List[str]] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        submitTimeBegin: Optional[str] = None,
        submitTimeEnd: Optional[str] = None,) -> dict:
    """
    盘点-盘点单-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        documentNo (str, None): 单据号. Defaults to None.
        planNo (str, None): 盘点计划单号. Defaults to None.
        createName (str, None): 制单人. Defaults to None.
        submitName (str, None): 提交人. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        inventoryType (int, None): 盘点类型. Defaults to None.
            - 可选值：1-抽盘，2-全盘，3-随机盘，5-动销盘，6-中药盘，7-非中药盘，8-柜组盘，9-品类盘
        statusList (List[str], None): 盘点状态. Defaults to None.
            - 可选值：["INVENTORYTAKING"," INVENTORIED"]-盘点中，["COMPLETED"]-盘点完成,["CANCEL"]-已作废
        genProfitLoss (int, None): 生成盈亏单. Defaults to None.
            - 可选值：1-是，0-否
        allocationTypes (List[str], None): 货位类型. Defaults to None.
            - 可选值：space_pass-合格，space_fail-不合格，space_tested-待检，space_medicine-中药，space_disassemble-拆零
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_store_warehouse(门店仓库) 与 select_warehouse(仓库) 中获取
        areaIds (List[str], None): 库区ID列表. Defaults to None.
            - 可在 warehouse_area_list 中获取
        cabinetIds (List[str], None): 柜组ID列表. Defaults to None.
            - 可在 warehouse_cabinet_list 中获取
        goodsIdList (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
        allocationIds (List[str], None): 货位ID列表. Defaults to None.
            - 可在 warehouse_allocation_list 中获取
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - 可在 store_region_tree 中获取
        createTimeBegin (str, None): 创建时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 创建时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeBegin (str, None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str, None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 盘点-盘点单-按商品响应体
    """
    if warehouseIdList is None:
        raise ValueError("warehouseIdList 不能为空")
    url = f"{base_url}TakingDtl/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "objectType": 3,
        "documentNo": documentNo,
        "planNo": planNo,
        "createName": createName,
        "submitName": submitName,
        "batchNo": batchNo,
        "inventoryType": inventoryType,
        "statusList": statusList,
        "genProfitLoss": genProfitLoss,
        "allocationTypes": allocationTypes,
        "warehouseIdList": warehouseIdList,
        "areaIds": areaIds,
        "cabinetIds": cabinetIds,
        "goodsIdList": goodsIdList,
        "allocationIds": allocationIds,
        "regionIdList": regionIdList,
        "createTimeBegin": createTimeBegin if createTimeBegin else taday,
        "createTimeEnd": createTimeEnd if createTimeEnd else taday,
        "submitTimeBegin": submitTimeBegin,
        "submitTimeEnd": submitTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()

async def inventory_profit_loss_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        total: bool = False,
        current: int = 1,
        size: int = 20,
        planNo: Optional[str] = None,
        batchNo: Optional[str] = None,
        batch: Optional[str] = None,
        profitLossStatusList: Optional[List[int]] = None,
        profitLossStatus: Optional[int] = None,
        adoptFlag: Optional[str] = None,
        inventoryType: Optional[int] = None,
        allocationTypes: Optional[List[str]] = None,
        source: Optional[str] = None,
        warehouseIdList: Optional[List[str]] = None,
        objectCodes: Optional[List[str]] = None,
        allocationIds: Optional[List[str]] = None,
        areaIds: Optional[List[str]] = None,
        cabinetIds: Optional[List[str]] = None,
        regionIdList: Optional[List[str]] = None,
        createTimeStart: Optional[str] = None,
        createTimeEnd: Optional[str] = None,
        inventoryTimeStart: Optional[str] = None,
        inventoryTimeEnd: Optional[str] = None,) -> dict:
    """
    盘点-盈亏单、库存调整记录
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户ID. Defaults to None.
        total (bool): 是否汇总. Defaults to False.
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20. 
        planNo (str, None): 盘点计划单号. Defaults to None.
        batchNo (str, None): 生产批号. Defaults to None.
        batch (str, None): 批次号. Defaults to None.
        profitLossStatusList (List[int], None): 盈亏状态. 可选值：0-盘亏，1-盘盈，-1-无差异. Defaults to None.
            - 可选值：0-盘亏，1-盘盈，-1-无差异
        profitLossStatus (int, None): 盈亏状态. Defaults to None.
            - 可选值：0-盘亏，1-盘盈
        adoptFlag (str, None): 产生盈亏. 可选值：true-是，false-否. Defaults to None.
            - 可选值：true-是，false-否
        inventoryType (int, None): 盘点类型. Defaults to None.
            - 可选值：1-抽盘，2-全盘，3-随机盘，5-动销盘，6-中药盘，7-非中药盘，8-柜组盘，9-品类盘
        allocationTypes (List[str], None): 货位类型. Defaults to None.
            - 可选值：space_pass-合格，space_fail-不合格，space_tested-待检，space_medicine-中药，space_disassemble-拆零
        source (str, None): 来源. Defaults to None.
            - 可选值：adopt-盘点盈亏，corrections-库存调整记录
        warehouseIdList (List[str], None): 仓库ID列表. Defaults to None.
            - 可在 select_store_warehouse(门店仓库) 与 select_warehouse(仓库) 中获取
        objectCodes (List[str], None): 商品编码列表. Defaults to None.
        allocationIds (List[str], None): 货位ID列表. Defaults to None.
            - 可在 warehouse_allocation_list 中获取
        areaIds (List[str], None): 库区ID列表. Defaults to None.
            - 可在 warehouse_area_list 中获取
        cabinetIds (List[str], None): 柜组ID列表. Defaults to None.
            - 可在 warehouse_cabinet_list 中获取
        regionIdList (List[str], None): 区域ID列表. Defaults to None.
            - 可在 store_region_tree 中获取
        createTimeStart (str, None): 制单时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 制单时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        inventoryTimeStart (str, None): 盘点时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        inventoryTimeEnd (str, None): 盘点时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 盘点-盈亏单响应体
    """
    if total:
        url = f"{base_url}ProfitLoss/getTotal"
    else:
        url = f"{base_url}ProfitLoss/page"

    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()
    payload = {
        "current": current,
        "size": size,
        "objectType": "3",
        "frontRequestFlag": 1,
        "planNo": planNo,
        "batchNo": batchNo,
        "batch": batch,
        #! 以下3个参数明明就是重复的，脱裤子放屁，多此一举
        "profitLossStatusList": profitLossStatusList,
        "profitLossStatus": profitLossStatus,
        "adoptFlag": adoptFlag,
        "inventoryType": inventoryType,
        "allocationTypes": allocationTypes,
        "source": source,
        "warehouseIdList": warehouseIdList,
        "objectCodes": objectCodes,
        "allocationIds": allocationIds,
        "areaIds": areaIds,
        "cabinetIds": cabinetIds,
        "regionIdList": regionIdList,
        "createTimeStart": createTimeStart if createTimeStart else taday,
        "createTimeEnd": createTimeEnd if createTimeEnd else taday,
        "inventoryTimeStart": inventoryTimeStart,
        "inventoryTimeEnd": inventoryTimeEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
