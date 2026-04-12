"""
供应商商品
    - 供应商商品列表: supplier_goods_list
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, retrieve_past_date


base_url = f"{yaoud_env['url']}/cp/supplierGoods"


async def supplier_goods_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: int = 1,
    size: int = 20,
    stockTimeBegin: str = retrieve_past_date(1),
    stockTimeEnd: Optional[str] = get_current_date(),
    supplierIds: Optional[List[str]] = None,
    classTypeIds: Optional[List[int]] = None,
    purchaserId: Optional[str] = None,
    purchaserStatus: Optional[int] = None,
    warehouseId: Optional[str] = None,)->dict:
    """
    可供品种-供应商商品列表
    Args:
        authorization (str): 授权token
        tenant_id (int): 租户id
        current (int): 当前页码. Defaults to 1.
        size (int): 每页数量. Defaults to 20.
        stockTimeBegin (str): 最后入库时间区间-开始. Defaults to 前1天.
            - 日期格式为yyyy-MM-dd
        stockTimeEnd (str,None): 最后入库时间区间-结束. Defaults to 当前日期.
            - 日期格式为yyyy-MM-dd
        supplierIds (List[str],None): 供应商ID列表. Defaults to None.
            - 可在 get_supplier_list 中获取.
        classTypeIds (List[int],None): 商品分类ID列表.可在 user_product_class_tree 中获取. Defaults to None.
        purchaserId (str,None): 采购员ID. Defaults to None.
            - 可在 get_employee_list 中获取 postCodes=POST_BUYER.
        purchaserStatus (int,None): 采购状态. Defaults to None.
            - (1:正常,0:停止采购)
        warehouseId (str,None): 仓库ID. Defaults to None.
            - 可在 select_warehouse 中获取.
    Returns:
        dict: 供应商商品列表
    """
    url = f"{base_url}/page"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "stockTimeBegin": stockTimeBegin,
        "stockTimeEnd": stockTimeEnd,
        "supplierIds": supplierIds,
        "classTypeIds": classTypeIds,
        "purchaserId": purchaserId,
        "purchaserStatus": purchaserStatus,
        "warehouseId": warehouseId,
    }
    async with AsyncClient() as client:
        response = await client.get(
            url, headers=headers,
            params=payload,timeout=yaoud_env["timeout"])
    return response.json()
