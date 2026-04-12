"""
供应商管理
    - 供应商信息列表-下拉检索用-带委托人: get_supplier_info_list
    - 供应商列表-下拉检索用: get_supplier_list
    - 简易供应商列表: simple_supplier_page
    - 供应商分类查询-下拉检索用: supplier_class_type
    - 供应商列表-下拉检索用: supplier_list
    - 供应商管理: supplier_page_list
    - 供应商管理-详情: supplier_info_detail
    - 供应商部门列表: supplier_dept_page
    - 供应商部门详情: supplier_dept_info
    - 合作商列表: partner_page_list
    - 合作商详情: partner_info_detail
    - 合作商分类树: partner_class_tree
"""

from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/supplier/bs"


async def get_supplier_info_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    供应商信息列表-下拉检索用-带委托人

    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户id. Defaults to None.
        keyword (str,None): 供应商名称关键词. Defaults to None.
            - 支持供应商名称、供应商编号、助记码

    Returns:
        dict: 供应商列表
    """
    url = f"{base_url}/external/supplier/getSupplierListIsGspinfo"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "keyWord": keyword,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])

    return response.json()


async def get_supplier_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        keyword: Optional[str] = None,) -> dict:
    """
    供应商列表-下拉检索用
    Args:
        authorization (str): 授权token
        tenant_id (int, None): 租户id. Defaults to None.
        keyword (str,None): 供应商名称关键词. Defaults to None.
            - 支持供应商名称、供应商编号、助记码
    Returns:
    """
    url = f"{base_url}/external/supplier/getSupplierList"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "keyword": keyword,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])

    return response.json()


async def simple_supplier_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,) -> dict:
    """
    简易供应商列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        keyword (str,None): 关键词. Defaults to None.
            - 支持供应商名称、供应商编号、助记码
    Returns:
        dict: 简易供应商列表
    """
    url = f"{base_url}/external/supplier/selectSimpleSupplierPage"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "keyword": keyword,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_class_type(
        authorization: str,
        tenant_id: Optional[int] = None,
        dataType: str = "gr_supplier") -> dict:
    """
    供应商分类查询-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        dataType (str): 数据类型. Defaults to "gr_supplier".
    Returns:
        dict: 分类查询-下拉检索用
    """
    url = f"{base_url}/supplierClassType/queryTree"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "dataType": dataType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])

    return response.json()


async def supplier_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        codes: Optional[List[str]] = None,) -> dict:
    """
    供应商列表-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 是否当前供应商. Defaults to None.
        size (int, None): 分页大小. Defaults to None.
        keyword (str,None): 供应商名称关键词. Defaults to None.
            - 支持供应商名称、供应商编号、助记码
        codes (List[str], None): 供应商分类编码列表. Defaults to None.
    Returns:
        dict: 供应商列表
    """
    url = f"{base_url}/external/supplier/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "codes": codes,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_page_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        vendorName: Optional[str] = None,
        vendorAbc: Optional[str] = None,
        socialCreditCode: Optional[str] = None,
        addr: Optional[str] = None,
        registeredAddressTwo: Optional[str] = None,
        warehouseAddress: Optional[str] = None,
        enterpriseHead: Optional[str] = None,
        legalRepresentative: Optional[str] = None,
        qualityHead: Optional[str] = None,
        capital: Optional[str] = None,
        badRecord: Optional[str] = None,
        status: Optional[str] = None,
        remark: Optional[str] = None,
        searchKeywordList: Optional[List[str]] = None,
        accountName: Optional[str] = None,
        bankDeposit: Optional[str] = None,
        bankAccount: Optional[str] = None,
        archivesCode: Optional[str] = None,
        vendorSupervise: Optional[str] = None,

        taxMethods: Optional[List[str]] = None,
        vendorTypes: Optional[List[str]] = None,
        isEnables: Optional[List[int]] = None,
        isPurchases: Optional[List[int]] = None,
        isOnlines: Optional[List[int]] = None,
        isGspinfos: Optional[List[int]] = None,
        isSynergys: Optional[List[int]] = None,
        minValidityDays: Optional[int] = None,
        maxValidityDays: Optional[int] = None,
        minDeliveryCycle: Optional[int] = None,
        maxDeliveryCycle: Optional[int] = None,

        transports: Optional[List[str]] = None,
        productTypeList: Optional[List[str]] = None,
        subcategorys: Optional[List[str]] = None,
        purchaseIds: Optional[List[str]] = None,
        createIds: Optional[List[str]] = None,
        updateIds: Optional[List[str]] = None,
        codes: Optional[List[str]] = None,
        prefixCode: Optional[str] = None,
        labelIds: Optional[List[str]] = None,
        synergyWarehouseId: Optional[List[str]] = None,
        synergyType: Optional[List[str]] = None,
        payments: Optional[List[str]] = None,
        payPeriods: Optional[List[str]] = None,
        invoiceTypes: Optional[List[str]] = None,
        manageMethods: Optional[List[str]] = None,

        startCompanyCreateDate: Optional[str] = None,
        endCompanyCreateDate: Optional[str] = None,
        startGspinfoDate: Optional[str] = None,
        endGspinfoDate: Optional[str] = None,
        startCreateTime: Optional[str] = None,
        endCreateTime: Optional[str] = None,
        startUpdateTime: Optional[str] = None,
        endUpdateTime: Optional[str] = None,) -> dict:
    """
    供应商管理
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 分页大小. Defaults to 20.
        vendorName (str, None): 供应商名称. Defaults to None.
        vendorAbc (str, None): 供应商助名称记码. Defaults to None.
        socialCreditCode (str, None): 社会信用代码. Defaults to None.
        addr (str, None): 地址. Defaults to None.
        registeredAddressTwo (str, None): 注册地址二. Defaults to None.
        warehouseAddress (str, None): 仓库地址. Defaults to None.
        enterpriseHead (str, None): 企业负责人. Defaults to None.
        legalRepresentative (str, None): 法定代表人. Defaults to None.
        qualityHead (str, None): 质量负责人. Defaults to None.
        capital (str, None): 注册资本. Defaults to None.
        badRecord (str, None): 不良记录. Defaults to None.
        searchKeywordList (str, None): 搜索关键词列表. Defaults to None.
        accountName (str, None): 账户名称. Defaults to None.
        bankDeposit (str, None): 开户行. Defaults to None.
        bankAccount (str, None): 银行账号. Defaults to None.
        archivesCode (str, None): 档案编号. Defaults to None.
        vendorSupervise (str, None): 供应商监管. Defaults to None.
        taxMethods (List[str], None): 纳税性质. Defaults to None.
            - ["一般纳税人", "小规模纳税人"]
        vendorTypes (List[str], None): 供应商类型. Defaults to None.
            - 1-生产企业
            - 2-普通经营企业
        isEnables (List[int], None): 供应商是否启用. Defaults to None.
            - 1-启用
            - 0-停用
        isPurchases (List[int], None): 是否允许采购. Defaults to None.
            - 1-允许
            - 0-不允许
        isOnlines (List[int], None): 是否线上供应商. Defaults to None.
            - 1-是
            - 0-否
        isGspinfos (List[int], None): 是否已首营. Defaults to None.
            - 1-是
            - 0-否
        isSynergys (List[int], None): 是否协同仓库. Defaults to None.
            - 1-是
            - 0-否
        minValidityDays (int, None): 送货周期区间-最小值. Defaults to None
        maxValidityDays (int, None): 送货周期区间-最大值. Defaults to None
        minDeliveryCycle (int, None): 订单效期区间-最小值. Defaults to None
        maxDeliveryCycle (int, None): 订单效期区间-最大值. Defaults to None
        transports (List[str], None): 运输方式. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为承运方式.
        productTypeList (List[str], None): 商品类型.可在 dict_item_list 中获取 keyword 为商品类型. Defaults to None
        subcategorys (List[str], None): 供应商分类. Defaults to None.
            - 可在 supplier_class_type 中获取，dataType=gr_supplier.
        purchaseIds (List[str], None): 负责采购员id. Defaults to None.
            - 可在 employee_page 中获取，对应字段id.
        createIds (List[str], None): 创建人ID. Defaults to None.
            - 可在 employee_page 中获取，对应字段id.
        updateIds (List[str], None): 更新人ID. Defaults to None.
            - 可在 employee_page 中获取，对应字段id.
        codes (List[str], None): 供应商编码. Defaults to None.
            - 可在 supplier_list 中获取.
        prefixCode (str, None): 所在区域编码.可在 region_tree 中获取. Defaults to None
        labelIds (List[str], None): 供应商标签id. Defaults to None.
            - 可在 goods_label_type_tree 中获取.
        synergyWarehouseId (List[str], None): 协同仓库id. Defaults to None.
            - 可在 synergys_warehouse_info 中获取.
        synergyType (List[str], None): 协同类型. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为协同类型.
        payments (List[str], None): 付款方式. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为付款方式.
        payPeriods (List[str], None): 付款账期. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为付款账期.
        invoiceTypes (List[str], None): 发票类型. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为发票类型.
        manageMethods (List[str], None): 经营方式. Defaults to None.
            - 可在 dict_item_list 中获取 keyword 为经营方式.
        startCompanyCreateDate (str, None): 企业成立区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        endCompanyCreateDate (str, None): 企业成立区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        startGspinfoDate (str, None): 首营时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        endGspinfoDate (str, None): 首营时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        startCreateTime (str, None): 创建时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        endCreateTime (str, None): 创建时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
        startUpdateTime (str, None): 更新时间区间-开始. Defaults to None.
            - 格式: yyyy-MM-dd
        endUpdateTime (str, None): 更新时间区间-结束. Defaults to None.
            - 格式: yyyy-MM-dd
    Returns:
        dict: 供应商列表
    """
    url = f"{base_url}/supplier/pageListNew"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }

    if startCreateTime:
        startCreateTime = get_date_start_and_end_time(startCreateTime)
    if endCreateTime:
        endCreateTime = get_date_start_and_end_time(endCreateTime)
    if startUpdateTime:
        startUpdateTime = get_date_start_and_end_time(startUpdateTime)
    if endUpdateTime:
        endUpdateTime = get_date_start_and_end_time(endUpdateTime)

    payload = {
        "current": current,
        "size": size,
        "vendorName": vendorName,
        "vendorAbc": vendorAbc,
        "socialCreditCode": socialCreditCode,
        "addr": addr,
        "registeredAddressTwo": registeredAddressTwo,
        "warehouseAddress": warehouseAddress,
        "enterpriseHead": enterpriseHead,
        "legalRepresentative": legalRepresentative,
        "qualityHead": qualityHead,
        "capital": capital,
        "badRecord": badRecord,
        "status": status,
        "remark": remark,
        "searchKeywordList": searchKeywordList,
        "accountName": accountName,
        "bankDeposit": bankDeposit,
        "bankAccount": bankAccount,
        "archivesCode": archivesCode,
        "vendorSupervise": vendorSupervise,
        "taxMethods": taxMethods,
        "vendorTypes": vendorTypes,
        "isEnables": isEnables,
        "isPurchases": isPurchases,
        "isOnlines": isOnlines,
        "isGspinfos": isGspinfos,
        "isSynergys": isSynergys,
        "minValidityDays": minValidityDays,
        "maxValidityDays": maxValidityDays,
        "minDeliveryCycle": minDeliveryCycle,
        "maxDeliveryCycle": maxDeliveryCycle,
        "transports": transports,
        "productTypeList": productTypeList,
        "subcategorys": subcategorys,
        "purchaseIds": purchaseIds,  # ! 在调用该接口时，postCodeList参数已经失效，查找的是所有人员
        "createIds": createIds,
        "updateIds": updateIds,
        "codes": codes,
        "prefixCode": prefixCode,
        "labelIds": labelIds,
        "synergyWarehouseId": synergyWarehouseId,
        "synergyType": synergyType,
        "payments": payments,
        "payPeriods": payPeriods,
        "invoiceTypes": invoiceTypes,
        "manageMethods": manageMethods,
        "startCompanyCreateDate": startCompanyCreateDate['start_time'] if startCompanyCreateDate else None,
        "endCompanyCreateDate": endCompanyCreateDate['end_time'] if endCompanyCreateDate else None,
        "startGspinfoDate": startGspinfoDate['start_time'] if startGspinfoDate else None,
        "endGspinfoDate": endGspinfoDate['end_time'] if endGspinfoDate else None,
        "startCreateTime": startCreateTime['start_time'] if startCreateTime else None,
        "endCreateTime": endCreateTime['end_time'] if endCreateTime else None,
        "startUpdateTime": startUpdateTime['start_time'] if startUpdateTime else None,
        "endUpdateTime": endUpdateTime['end_time'] if endUpdateTime else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_info_detail(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    供应商管理-详情
    Args:
        authorization (str): 认证信息
        id (str): 供应商ID. Defaults to None.
            - 可在 supplier_page_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商管理-详情
    """
    url = f"{base_url}/supplier/info"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_dept_page(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        enabled: Optional[int] = None,) -> dict:
    """
    供应商部门列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 分页大小. Defaults to 20.
        keyword (str, None): 关键字检索. Defaults to None.
        enabled (int, None): 是否启用. Defaults to None.
    Returns:
        dict: 供应商部门列表
    """
    url = f"{base_url}/supplier/dept/page"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "current": current,
        "size": size,
        "keyword": keyword,
        "enabled": enabled,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def supplier_dept_info(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    供应商部门详情
    Args:
        authorization (str): 认证信息
        id (str): 供应商部门ID. Defaults to None.
            - 可在 supplier_dept_page 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 供应商部门详情
    """
    url = f"{base_url}/supplier/dept/info"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "id": id,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()


async def partner_page_list(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        classId: Optional[str] = None,
        keyword: Optional[str] = None,
        isEnable: Optional[int] = None,) -> dict:
    """
    合作商列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 分页大小. Defaults to 20.
        classId (str, None): 合作商分类ID. Defaults to None.
        keyword (str, None): 关键字检索. Defaults to None.
        isEnable (int, None): 是否启用. Defaults to None.
    Returns:
        dict: 合作商列表
    """
    url = f"{base_url}/partner/pageList"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    payload = {
        "current": current,
        "size": size,
        "classId": classId,
        "keyword": keyword,
        "isEnable": isEnable,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=yaoud_env["timeout"])
    return response.json()


async def partner_info_detail(
        authorization: str,
        id: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    合作商详情
    Args:
        authorization (str): 认证信息
        id (str): 合作商ID. Defaults to None.
            - 可在 partner_page_list 中获取，对应字段id.
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 合作商详情
    """
    url = f"{base_url}/partner/info/{id}"
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


async def partner_class_tree(
        authorization: str,
        tenant_id: Optional[int] = None,
        dataType: str = "bs_partner",) -> dict:
    """
    合作商分类树
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        dataType (str): 数据类型. Defaults to "bs_partner".
    Returns:
        dict: 合作商分类树
    """
    url = f"{base_url}/partnerClassType/queryTree"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "dataType": dataType,
        "_t": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=yaoud_env["timeout"])
    return response.json()
