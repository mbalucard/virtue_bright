"""
店铺商品
    - 商品异常类型-枚举值: unusual_info_enum
    - 店铺商品管理: shop_product_page
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/shopProduct/rlShopProduct"
TTL = yaoud_env["timeout"]


async def unusual_info_enum(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    商品异常类型-枚举值
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 枚举值
    """
    #! 枚举值 暂未使用，本接口在店铺商品管理中找到，疑似与unusual参数联动
    url = f"{base_url}/getUnusualInfoEnum"
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


async def shop_product_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        name: Optional[str] = None,
        barcode: Optional[str] = None,
        producer: Optional[str] = None,
        licenseNumber: Optional[str] = None,
        proStatus: Optional[int] = None,
        unusual: Optional[int] = None,
        isSpecialPrice: Optional[int] = None,
        isMaintainPrice: Optional[int] = None,
        isMedicalCustom: Optional[int] = None,
        isMedicare: Optional[int] = None,
        codes: Optional[List[str]] = None,
        shopType: Optional[int] = None,
        shopId: Optional[int] = None,
        storeCode: Optional[str] = None,
        proPriceMin: Optional[int] = None,
        proPriceMax: Optional[int] = None,
        proStockMin: Optional[int] = None,
        proStockMax: Optional[int] = None,) -> dict:
    """
    店铺商品管理
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页条目数最大100. Defaults to 20.
        name (str, None): 商品名称. Defaults to None.
        barcode (str, None): 国际条码. Defaults to None.
        producer (str, None): 生产企业. Defaults to None.
        licenseNumber (str, None): 批准文号. Defaults to None.
        proStatus (int, None): 商品状态. Defaults to None.
            - 1-上架
            - 0-下架
        unusual (int, None): 异常状态. Defaults to None.
            - 1-异常
            - 0-正常
        isSpecialPrice (int, None): 是否特价商品. Defaults to None.
            - 1-是
            - 0-否
        isMaintainPrice (int, None): 是否维价商品. Defaults to None.
            - 1-是
            - 0-否
        isMedicalCustom (int, None): 是否启用自定义医保. Defaults to None.
            - 1-是
            - 0-否
        isMedicare (int, None): 是否医保品种. Defaults to None.
            - 1-是
            - 0-否
        codes (List[str], None): 商品编码列表. Defaults to None.
            - 可在 external_goods_page_list 中获取.
        shopType (int, None): 店铺类型. Defaults to None.
            - 可在 shop_config_desc_list 中获取.
        shopId (int, None): 店铺ID. Defaults to None.
            - 可在 shop_config_page_list 中获取.
        storeCode (str, None): 参与门店编码. Defaults to None.
            - 可在 select_stores 中获取.
        proPriceMin (int, None): 商品价格区间-最小值. Defaults to None.
        proPriceMax (int, None): 商品价格区间-最大值. Defaults to None.
        proStockMin (int, None): 商品库存区间-最小值. Defaults to None.
        proStockMax (int, None): 商品库存区间-最大值. Defaults to None.
    Returns:
        dict: 店铺商品管理
    """
    url = f"{base_url}/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "name": name,  # ! 和 codes 参数功能一样，且还不能多选，这个参数还在用，难道是混绩效的么
        "barcode": barcode,
        "producer": producer,
        "licenseNumber": licenseNumber,
        "proStatus": proStatus,
        "unusual": unusual,  # ! 光有异常，异常原因还没有，做东西做一半，哎。。。
        "isSpecialPrice": isSpecialPrice,
        "isMaintainPrice": isMaintainPrice,
        "isMedicalCustom": isMedicalCustom,
        "isMedicare": isMedicare,
        "codes": codes,
        "shopType": shopType,
        "shopId": shopId,
        "storeCode": storeCode,  # ! 与 shopId 参数功能一样，且还不能和 shopType 联动使用，真不知道有啥用，还不从产线拿掉。
        "proPriceMin": proPriceMin,
        "proPriceMax": proPriceMax,
        "proStockMin": proStockMin,
        "proStockMax": proStockMax,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
