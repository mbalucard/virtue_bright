"""
药德商品库
    - 商品列表查询(药德标品库): yd_goods_list
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/product/yd"
TTL = yaoud_env["timeout"]


async def yd_goods_list(
        authorization: str,
        tenant_id: Optional[str] = None,
        current: int = 1,
        size: int = 20,
        keywordNew: Optional[str] = None,
        barcode: Optional[str] = None,
        productType: Optional[str] = None,
        licenseNumber: Optional[str] = None,
        spec: Optional[str] = None,
        breedCode: Optional[str] = None,
        producer: Optional[str] = None,
        proAddress: Optional[str] = None):
    """
    商品列表查询(药德标品库)
    Args:
        authorization (str): 授权token，格式为"Bearer <token>"
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int): 当前页. Defaults to 1.
        size (int): 每页数据数量，最大100. Defaults to 20.
        keywordNew (str, None): 商品关键词. Defaults to None.
            - 商品名称，商品编码，助记码
        barcode (str, None): 商品条码. Defaults to None.
        productType (str, None): 商品类型. Defaults to None.
            - 可在 dict_item_list 中获取, keyword=商品类型
        licenseNumber (str, None): 批准文号/注册证号/备案号. Defaults to None.
        spec (str, None): 商品规格. Defaults to None.
        breedCode (str, None): 国家医保编码. Defaults to None.
        producer (str, None): 生产企业. Defaults to None.
        proAddress (str, None): 产地. Defaults to None.
    Returns:
        dict: 商品列表json响应体
    """
    url = f"{base_url}/ydGoods/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "keywordNew": keywordNew,
        "barcode": barcode,
        "licenseNumber": licenseNumber,
        "spec": spec,
        "breedCode": breedCode,
        "producer": producer,
        "proAddress": proAddress,
        "_t": timestamp(),
    }
    #! 用来处理productType参数为空或None时，都不能出现的情况，否则没数据，写接口的绝对是个白痴
    if productType:
        params["productType"] = productType
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()
