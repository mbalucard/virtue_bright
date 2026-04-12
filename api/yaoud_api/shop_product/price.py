"""
价格管理
    - 零售价格组-价格组: pric_group_page
    - 零售价格组-商品明细: pric_group_detail_list
    - 调价来源-下拉检索用: price_record_source
    - 调价类型-下拉检索用: price_record_type
    - 调价单状态-下拉检索用: price_record_status
    - 零售价格组-调价记录: price_record_page
    - 零售价格组-调价记录-基本信息详情: price_record_basic_info
    - 零售价格组-调价记录-商品信息详情: price_record_bills_list
    - 零售价格组-商品调价单: price_prodct_record_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/shopProduct/rlPrice"
TTL = yaoud_env["timeout"]


async def pric_group_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        groupName: Optional[str] = None,
        storeId: Optional[int] = None,
        shopType: Optional[int] = None,) -> dict:
    """
    零售价格组-价格组
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        groupName (str, None): 价格组名称. Defaults to None.
        storeId (int, None): 门店ID. Defaults to None.
            - 可在 get_stores 中获取对应字段ID，如店铺类型不为None，则在 shop_config_page_list 中获取.
        shopType (int, None): 店铺类型编码. Defaults to None.
            - 可在 shop_config_desc_list 中获取.
    Returns:
        dict: 零售价格组-价格组
    """
    url = f"{base_url}Group/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "groupName": groupName,
        "storeId": storeId,
        "shopType": shopType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def pric_group_detail_list(
        authorization: str,
        priceGroupId: int,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        productTypes: Optional[List[str]] = None,
        isMaintainPrice: Optional[int] = None,
        isSpecialPrice: Optional[int] = None,
        isSplit: Optional[int] = None,
        isHaveProPrice: Optional[int] = None,
        isEnable: Optional[int] = None,) -> dict:
    """
    零售价格组-商品明细
    Args:
        authorization (str): 认证信息
        priceGroupId (int): 价格组ID. Defaults to None.
            - 可在 pric_group_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        keyword (str, None): 关键字搜索. Defaults to None.
            - 支持商品编码、商品名称、助记码、生产企业的模糊查找.
        productTypes (List[str], None): 商品类型. Defaults to None.
            - 可在 dict_item_list 中获取.
        isMaintainPrice (int, None): 是否维价商品. Defaults to None.
            - 0-否
            - 1-是
        isSpecialPrice (int, None): 是否特价商品. Defaults to None.
            - 0-否
            - 1-是
        isSplit (int, None): 是否拆零商品. Defaults to None.
            - 0-否
            - 1-是
        isHaveProPrice (int, None): 是否存在零售价. Defaults to None.
            - 0-否
            - 1-是
        isEnable (int, None): 是否启用. Defaults to None.
            - 0-否
            - 1-是
    Returns:
        dict: 零售价格组-商品明细
    """
    url = f"{base_url}GroupDetail/listBsGoods"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "priceGroupId": priceGroupId,
        "keyword": keyword,
        "productTypes": productTypes,
        "isMaintainPrice": isMaintainPrice,
        "isSpecialPrice": isSpecialPrice,
        "isSplit": isSplit,
        "isHaveProPrice": isHaveProPrice,
        "isEnable": isEnable,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_record_source(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    调价来源-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 调价来源-下拉检索用
    """
    url = f"{base_url}Record/source"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_record_type(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    调价类型-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 调价类型-下拉检索用
    """
    url = f"{base_url}Record/recordType"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_record_status(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    调价单状态-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 调价单状态-下拉检索用
    """
    url = f"{base_url}Record/recordStatus"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_record_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        recordOdd: Optional[int] = None,
        source: Optional[int] = None,
        recordStatus: Optional[int] = None,
        recordTypes: Optional[int] = None,
        proId: Optional[str] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,
        startExecuteTime: Optional[str] = None,
        endExecuteTime: Optional[str] = None,) -> dict:
    """
    零售价格组-调价记录
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
        recordOdd (int, None): 调价单号. Defaults to None.
        source (int, None): 调价来源. Defaults to None.
            - 可在 price_record_source 中获取.
        recordStatus (int, None): 调价单状态. Defaults to None.
            - 1-审批中
            - 2-待生效
            - 3-已生效
            - 4-已取消
            - 5-驳回
        recordTypes (int, None): 调价类型. Defaults to None.
            - 可在 price_record_type 中获取.
        proId (str, None): 商品ID. Defaults to None.
            - 可在 external_goods_page_list 中获取.
        startTime (str, None): 创建时间区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endTime (str, None): 创建时间区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
        startExecuteTime (str, None): 生效时间区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endExecuteTime (str, None): 生效时间区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    Returns:
        dict: 零售价格组-调价记录-列表
    """
    url = f"{base_url}Record/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if startTime:
        startTime = get_date_start_and_end_time(startTime)
    if endTime:
        #! 这里如果endTime不为None, startTime为None, 则是查询所有数据，真的很为公司悲哀
        endTime = get_date_start_and_end_time(endTime)
    elif startTime and not endTime:
        #! 后端未作处理，如果startTime有值，但endTime为None, 接口将查询所有数据，公司的服务器真的是不要钱啊
        # 这里给后端擦屁股，把endTime设置为当前日期
        taday = get_current_date()
        endTime = get_date_start_and_end_time(taday)

    if startExecuteTime:
        startExecuteTime = get_date_start_and_end_time(startExecuteTime)
    if endExecuteTime:
        #! 这里如果endTime不为None, startTime为None, 则是查询所有数据
        endExecuteTime = get_date_start_and_end_time(endExecuteTime)
    elif startExecuteTime and not endExecuteTime:
        #! 后端未作处理，如果startExecuteTime有值，但endExecuteTime为None, 接口将查询所有数据
        # 这里给后端擦屁股，把endExecuteTime设置为当前日期
        taday = get_current_date()
        endExecuteTime = get_date_start_and_end_time(taday)

    params = {
        "current": current,
        "size": size,
        "recordOdd": recordOdd,
        "source": source,
        "recordStatus": recordStatus,
        "recordTypes": recordTypes,
        "proId": proId,
        "startTime": startTime['start_time'] if startTime else None,
        "endTime": endTime['end_time'] if endTime else None,
        "startExecuteTime": startExecuteTime['start_time'] if startExecuteTime else None,
        "endExecuteTime": endExecuteTime['end_time'] if endExecuteTime else None,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_record_basic_info(
        authorization: str,
        priceRecordId: int | str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    零售价格组-调价记录-基本信息详情
    Args:
        authorization (str): 认证信息
        priceRecordId (int | str): 调价记录ID. Defaults to None.
            - 可在 price_record_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 零售价格组-调价记录-基本信息详情
    """
    url = f"{base_url}Record/getPriceRecord/{priceRecordId}"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_record_bills_list(
        authorization: str,
        priceRecordId: int | str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,) -> dict:
    """
    零售价格组-调价记录-商品信息详情
    Args:
        authorization (str): 认证信息
        priceRecordId (int | str): 调价记录ID. Defaults to None.
            - 可在 price_record_page 中获取.
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数. Defaults to 20.
    Returns:
        dict: 零售价格组-调价记录-商品信息详情
    """
    url = f"{base_url}Bills/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "priceRecordId": priceRecordId,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def price_prodct_record_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        groupCode: Optional[str] = None,
        proIds: Optional[List[str]] = None,
        source: Optional[int] = None,
        recordStatus: Optional[int] = None,
        recordTypes: Optional[int] = None,
        startExecuteTime: Optional[str] = None,
        endExecuteTime: Optional[str] = None,) -> dict:
    """
    零售价格组-商品调价单
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        groupCode (str, None): 零售价格组编码. Defaults to None.
            - 可在 pric_group_page 中获取.
        proIds (List[str], None): 商品ID列表. Defaults to None.
            - 可在 external_goods_page_list 中获取.
        source (int, None): 调价来源. Defaults to None.
            - 可在 price_record_source 中获取.
        recordStatus (int, None): 调价单状态. Defaults to None.
            - 可在 price_record_status 中获取.
        recordTypes (int, None): 调价类型. Defaults to None.
            - 可在 price_record_type 中获取.
        startExecuteTime (str, None): 生效时间区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endExecuteTime (str, None): 生效时间区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    Returns:
        dict: 零售价格组-商品调价单
    """
    url = f"{base_url}Bills/pagePriceProduct"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if startExecuteTime:
        startExecuteTime = get_date_start_and_end_time(startExecuteTime)

    if endExecuteTime:
        endExecuteTime = get_date_start_and_end_time(endExecuteTime)
    elif startExecuteTime and not endExecuteTime:
        #! 后端未作处理，如果startExecuteTime有值，但endExecuteTime为None, 接口将查询所有数据
        # 把endExecuteTime设置为当前日期
        taday = get_current_date()
        endExecuteTime = get_date_start_and_end_time(taday)

    params = {
        "current": current,
        "size": size,
        "groupCode": groupCode,
        "proIds": proIds,
        "source": source,
        "recordStatus": recordStatus,
        "recordTypes": recordTypes,
        "startExecuteTime": startExecuteTime['start_time'] if startExecuteTime else None,
        "endExecuteTime": endExecuteTime['end_time'] if endExecuteTime else None,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
