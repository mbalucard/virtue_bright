"""
配送价格
    - 配送价格组-价格组: ds_delivery_price
    - 配送价格组-已启用价格组-下拉检索用: ds_delivery_price_list
    - 配送价格组-价格组-关联门店: ds_delivery_price_store
    - 配送价格组-价格组-详情: ds_delivery_price_detail
    - 配送价格组-商品价格组列表: ds_delivery_adjust_goods
    - 配送价格组-商品调价单-按单据: ds_delivery_adjust_page
    - 配送价格组-商品调价单-按单据-详情: ds_delivery_adjust_detail
    - 配送价格组-商品调价单-按商品明细: ds_delivery_adjust_goods
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.yaoud import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time

base_url = f"{yaoud_env['url']}/distribution/dsDeliveryPrice"


async def ds_delivery_price(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        deliveryCode: Optional[str] = None,
        status: Optional[int] = None,
        createId: Optional[str] = None,
        priceIncreaseMethod: Optional[str] = None,
        createTimeBegin: Optional[str] = None,
        createTimeEnd: Optional[str] = None,) -> dict:
    """
    配送价格组-价格组
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        deliveryCode (str, None): 配送价格组编码.可在 ds_delivery_price_list 中获取 对应字段deliveryCode. Defaults to None.
            - 可在 ds_delivery_price_list 中获取 对应字段deliveryCode
        status (int, None): 状态. Defaults to None.
            - (0:启用中，1:已作废)
        createId (str, None): 创建人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        priceIncreaseMethod (str, None): 加价方式. 需要枚举值. Defaults to None.
        createTimeBegin (str, None): 创建时间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 创建时间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 配送价格组-价格组
    """
    url = f"{base_url}/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    # ! 这里两个时间参数，要么都为None, 要么都为有值，否则不返回数据
    if createTimeBegin:
        createTimeBegin = get_date_start_and_end_time(createTimeBegin)

    if createTimeEnd:
        createTimeEnd = get_date_start_and_end_time(createTimeEnd)
    else:
        taday = get_current_date()
        createTimeEnd = get_date_start_and_end_time(taday)

    params = {
        "current": current,
        "size": size,
        "deliveryCode": deliveryCode,
        "status": status,
        "createId": createId,
        "priceIncreaseMethod": priceIncreaseMethod,
        "createTimeBegin": createTimeBegin['start_time'] if createTimeBegin else None,
        "createTimeEnd": createTimeEnd['end_time'] if createTimeBegin else None,
        "_t": timestamp(),
    }

    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def ds_delivery_price_list(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    配送价格组-已启用价格组-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 配送价格组-已启用价格组-下拉检索用
    """
    url = f"{base_url}/list"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()



async def ds_delivery_price_store(
    authorization: str,
    ds_delivery_price_id: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    配送价格组-价格组-关联门店
    Args:
        authorization (str): 认证信息
        ds_delivery_price_id (int): 配送价格组ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 配送价格组-价格组-关联门店
    """

    url = f"{base_url}/getStore/{ds_delivery_price_id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def ds_delivery_price_detail(
    authorization: str,
    ds_delivery_price_id: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    配送价格组-价格组-详情
    Args:
        authorization (str): 认证信息
        ds_delivery_price_id (int): 配送价格组ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 配送价格组-价格组-详情
    """
    url = f"{base_url}/detail/{ds_delivery_price_id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, timeout=yaoud_env["timeout"])
    return response.json()


async def ds_delivery_adjust_goods(
    authorization: str,
    deliveryCode: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    goodsIds: Optional[List[str]] = None,)->dict:
    """
    配送价格组-商品价格组列表
    Args:
        authorization (str): 认证信息
        deliveryCode (str): 配送价格组编码. Defaults to None.
            - 可在 ds_delivery_price_list 中获取 对应字段deliveryCode
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        goodsIds (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取
    Returns:
        dict: 配送价格组-商品价格组列表
    """
    url = f"{base_url}Goods/pageDetailPost"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "status":"0",  #! 未知参数,疑似价格组状态 type: str
        "current": current,
        "size": size,
        "deliveryCode": deliveryCode,
        "goodsIds": goodsIds,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def ds_delivery_adjust_page(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    status: Optional[str] = None,
    createId: Optional[str] = None,
    createTimeBegin: Optional[str] = None,
    createTimeEnd: Optional[str] = None,)->dict:
    """
    配送价格组-商品调价单-按单据
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        status (str, None): 单据状态. Defaults to None.
            - (draft:草稿, in_approval:审核中, reject:已驳回, finish:已完成, cancel:已作废)
        createId (str, None): 创建人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        createTimeBegin (str, None): 创建时间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 创建时间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
    Returns:
        dict: 配送价格组-商品调价单-按单据
    """
    url = f"{base_url}Adjust/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createTimeBegin:
        createTimeBegin = get_date_start_and_end_time(createTimeBegin)
    if createTimeEnd:
        createTimeEnd = get_date_start_and_end_time(createTimeEnd)
    else:
        taday = get_current_date()
        createTimeEnd = get_date_start_and_end_time(taday)

    params = {
        "current": current,
        "size": size,
        "status": status,
        "createId": createId,
        "createTimeBegin": createTimeBegin['start_time'] if createTimeBegin else None,
        "createTimeEnd": createTimeEnd['end_time'] if createTimeEnd else None,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def ds_delivery_adjust_detail(
    authorization: str,
    ds_delivery_adjust_id: int,
    tenant_id: Optional[int] = None,) -> dict:
    """
    配送价格组-商品调价单-按单据-详情
    Args:
        authorization (str): 认证信息
        ds_delivery_adjust_id (int): 配送价格组ID
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 配送价格组-商品调价单-按单据-详情
    """
    url = f"{base_url}Adjust/detail/{ds_delivery_adjust_id}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=yaoud_env["timeout"])
    return response.json()


async def ds_delivery_adjust_goods(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    status: Optional[str] = None,
    createId: Optional[str] = None,
    goodsIds: Optional[List[str]] = None,
    deliveryCode: Optional[str] = None,
    createTimeBegin: Optional[str] = None,
    createTimeEnd: Optional[str] = None,
    beforeIncreaseMethod: Optional[str] = None,
    afterIncreaseMethod: Optional[str] = None,)->dict:
    """
    配送价格组-商品调价单-按商品明细
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        status (str, None): 单据状态. Defaults to None.
            - (draft:草稿, in_approval:审核中, reject:已驳回, finish:已完成, cancel:已作废)
        createId (str, None): 创建人ID. Defaults to None.
            - 可在 get_employee_list 中获取
        goodsIds (List[str], None): 商品ID列表.可在 external_goods_page_list 中获取. Defaults to None.
        deliveryCode (str, None): 配送价格组编码. Defaults to None.
            - 可在 ds_delivery_price_list 中获取 对应字段deliveryCode
        createTimeBegin (str, None): 创建时间-开始. Defaults to None.
            - 日期格式为yyyy-MM-dd
        createTimeEnd (str, None): 创建时间-结束. Defaults to None.
            - 日期格式为yyyy-MM-dd
        beforeIncreaseMethod (str, None): 调价方式-调价前. Defaults to None.
            - 需要枚举值
        afterIncreaseMethod (str, None): 调价方式-调价后. Defaults to None.
            - 需要枚举值
    Returns:
        dict: 配送价格组-商品调价单-按商品明细
    """
    url = f"{base_url}Adjust/pageDetail"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if createTimeBegin:
        createTimeBegin = get_date_start_and_end_time(createTimeBegin)
    if createTimeEnd:
        createTimeEnd = get_date_start_and_end_time(createTimeEnd)
    else:
        taday = get_current_date()
        createTimeEnd = get_date_start_and_end_time(taday)

    params = {
        "current": current,
        "size": size,
        "status": status,
        "createId": createId,
        "deliveryCode": deliveryCode,
        "createTimeBegin": createTimeBegin['start_time'] if createTimeBegin else None,
        "createTimeEnd": createTimeEnd['end_time'] if createTimeBegin else None,
        "_t": timestamp(),
    }

    if goodsIds:
        params["goodsIds"] = goodsIds
    if beforeIncreaseMethod:
        params["beforeIncreaseMethod"] = beforeIncreaseMethod
    if afterIncreaseMethod:
        params["afterIncreaseMethod"] = afterIncreaseMethod

    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()

