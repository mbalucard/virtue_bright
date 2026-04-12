"""
缺货
    - 缺货登记-按门店: stockout_registration_list
    - 缺货登记-按商品: stockout_registration_goods_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, retrieve_past_date


base_url = f"{yaoud_env['url']}/cp/stockout"



async def stockout_registration_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    createTimeStart: str = retrieve_past_date(1),
    createTimeEnd: Optional[str] = get_current_date(),
    submitTimeStart: Optional[str] = None,
    submitTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
    warehouseId: Optional[str] = None,
    goodsIdList: Optional[List[str]] = None,
    storeIds: Optional[List[str]] = None,
    createIds: Optional[List[str]] = None,
    isAllowBuy: Optional[int] = None,
    purchaserId: Optional[str] = None,
    stockoutNo: Optional[str] = None,
    purchasePlanNo: Optional[str] = None,
    submitUserName: Optional[str] = None,
    productType: Optional[str] = None,
    productSecondTypes: Optional[List[str]] = None,
    stockoutType: Optional[int] = None,
    customOne: Optional[str] = None,
    customTwo: Optional[str] = None,
    customThree: Optional[str] = None,
    customSix: Optional[str] = None,
    status: Optional[str] = None,)->dict:
    """
    缺货登记-按门店
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户id
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        createTimeStart (str): 制单时间区间-开始. Defaults to 前1天.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str,None): 制单时间区间-结束.日期格式为yyyy-MM-dd. Defaults to 当前日期.
        submitTimeStart (str,None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str,None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str,None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str,None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        warehouseId (str,None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取.
        goodsIdList (List[str],None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_llist 中获取.
        storeIds (List[str],None): 门店ID列表. Defaults to None.
            - 可在 select_store_warehouse 中找到，对应字段mainId.
        createIds (List[str],None): 制单人ID列表. Defaults to None.
            - 可在 get_employee_list 中获取，选择对应的 organIds.
        isAllowBuy (int,None): 是否允许采购. Defaults to None.
            - (1:是，0:否)
        purchaserId (str,None): 采购人ID. Defaults to None.
            - 可在 get_employee_list 中获取 postCodes=POST_BUYER.
        stockoutNo (str,None): 缺货登记编号. Defaults to None.
        purchasePlanNo (str,None): 采购计划编号. Defaults to None.
        submitUserName (str,None): 提交人姓名. Defaults to None.
        productType (str,None): 商品类型. Defaults to None.
        productSecondTypes (List[str],None): 商品二级类型列表. Defaults to None.
            - (0:中成药,1:化学药品,biological_products：生物制剂)
        stockoutType (int,None): 缺货登记类型. Defaults to None.
            - (0:商品缺货，1:赠品缺货)
        customOne (str,None): 自定义字段1. Defaults to None.
        customTwo (str,None): 自定义字段2. Defaults to None.
        customThree (str,None): 自定义字段3. Defaults to None.
        customSix (str,None): 自定义字段6. Defaults to None.
        status (str,None): 缺货登记状态. Defaults to None.
            - DRAFT:待采购，TO_PURCHASE：处理中，COMPLETED：已完成，CANCEL：已作废
    Returns:
        dict: 缺货登记列表
    """
    url = f"{base_url}/getPage"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "createTimeStart": createTimeStart,
        "createTimeEnd": createTimeEnd,
        "submitTimeStart": submitTimeStart,
        "submitTimeEnd": submitTimeEnd,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "warehouseId": warehouseId,
        "goodsIdList": goodsIdList,
        "storeIds": storeIds,
        "createIds": createIds,
        "isAllowBuy": isAllowBuy,
        "purchaserId": purchaserId,
        "stockoutNo": stockoutNo,
        "purchasePlanNo": purchasePlanNo,
        "submitUserName": submitUserName,
        "productType": productType,
        "productSecondTypes": productSecondTypes,
        "stockoutType": stockoutType,
        "customOne": customOne,
        "customTwo": customTwo,
        "customThree": customThree,
        "customSix": customSix,
        "status": status,
    }
    async with AsyncClient() as client:
        response = await client.post(
            url, headers=headers,
            json=payload,timeout=yaoud_env["timeout"])
    return response.json()


async def stockout_registration_goods_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    createTimeStart: str = retrieve_past_date(1),
    createTimeEnd: Optional[str] = get_current_date(),
    submitTimeStart: Optional[str] = None,
    submitTimeEnd: Optional[str] = None,
    takeEffectTimeStart: Optional[str] = None,
    takeEffectTimeEnd: Optional[str] = None,
    isAllowBuy: Optional[int] = None,
    goodsIdList: Optional[List[str]] = None,
    warehouseId: Optional[str] = None,
    purchaserId: Optional[str] = None,
    productType: Optional[str] = None,
    productSecondTypes: Optional[List[str]] = None,
    purchasePlanNo: Optional[str] = None,
    stockoutNo: Optional[str] = None,
    submitUserName: Optional[str] = None,
    customOne: Optional[str] = None,
    customTwo: Optional[str] = None,
    customThree: Optional[str] = None,
    customFour: Optional[str] = None,
    customSix: Optional[str] = None,
    status: Optional[str] = None,)->dict:
    """
    缺货登记-按商品
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户id
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        createTimeStart (str): 制单时间区间-开始. Defaults to 前1天.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str,None): 制单时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        submitTimeStart (str,None): 提交时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        submitTimeEnd (str,None): 提交时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeStart (str,None): 生效时间区间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        takeEffectTimeEnd (str,None): 生效时间区间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        isAllowBuy (int,None): 是否允许采购. Defaults to None.
            - (1:是，0:否)
        goodsIdList (List[str],None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_llist 中获取.
        productType (str,None): 商品类型. Defaults to None.
        productSecondTypes (List[str],None): 商品二级类型列表. Defaults to None.
            - (0:中成药,1:化学药品,biological_products：生物制剂)
        purchasePlanNo (str,None): 采购计划编号. Defaults to None.
        stockoutNo (str,None): 缺货登记编号. Defaults to None.
        submitUserName (str,None): 提交人姓名. Defaults to None.
        customOne (str,None): 自定义字段1. Defaults to None.
        customTwo (str,None): 自定义字段2. Defaults to None.
        customThree (str,None): 自定义字段3. Defaults to None.
        customFour (str,None): 自定义字段4. Defaults to None.
        customSix (str,None): 自定义字段6. Defaults to None.
        status (str,None): 缺货登记状态. Defaults to None.
            - DRAFT:待采购，TO_PURCHASE：处理中，COMPLETED：已完成，CANCEL：已作废
    Returns:
        dict: 缺货登记商品列表
    """
    url = f"{base_url}/getPageByGoods"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "createTimeStart": createTimeStart,
        "createTimeEnd": createTimeEnd,
        "submitTimeStart": submitTimeStart,
        "submitTimeEnd": submitTimeEnd,
        "takeEffectTimeStart": takeEffectTimeStart,
        "takeEffectTimeEnd": takeEffectTimeEnd,
        "isAllowBuy": isAllowBuy,
        "goodsIdList": goodsIdList,
        "warehouseId": warehouseId,
        "purchaserId": purchaserId,
        "productType": productType,
        "productSecondTypes": productSecondTypes,
        "purchasePlanNo": purchasePlanNo,
        "stockoutNo": stockoutNo,
        "submitUserName": submitUserName,
        "customOne": customOne,
        "customTwo": customTwo,
        "customThree": customThree,
        "customFour": customFour,
        "customSix": customSix,
        "status": status,
    }
    async with AsyncClient() as client:
        response = await client.post(
            url, headers=headers,
            json=payload,timeout=yaoud_env["timeout"])
    return response.json()
