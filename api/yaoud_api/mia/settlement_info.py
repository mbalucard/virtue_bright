"""
医保结算信息
    - 医保结算信息: settlement_info
    - 医保结算明细-商品: settlement_info_details
    - 医保对账记录: settlement_info_reconciliation
    - 医保清算记录查询: settlement_info_liquidation
    - 医保就诊类型占比: mdtrt_cert_type_count
    - 医保保障申报表: settlement_info_report
    - 按人员类型申报: report_list_by_user_type
"""


from httpx import AsyncClient
from typing import Optional, List

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import timestamp, get_current_date, get_date_start_and_end_time


base_url = f"{yaoud_env['url']}/mia/settlementInfo"
TTL = yaoud_env["timeout"]


async def settlement_info(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        certno: Optional[str] = None,
        agnterName: Optional[str] = None,
        agnterCertno: Optional[str] = None,
        insutype: Optional[str] = None,
        orgcodg: Optional[List[str]] = None,
        psnName: Optional[str] = None,
        setlIdBus: Optional[str] = None,
        setlId: Optional[str] = None,
        mdtrtId: Optional[str] = None,
        opterName: Optional[str] = None,
        clrOoptins: Optional[str] = None,
        medType: Optional[str] = None,
        clrType: Optional[str] = None,
        psnCertType: Optional[str] = None,
        mdtrtCertType: Optional[str] = None,
        diseCodg: Optional[str] = None,
        trnsState: Optional[str] = None,
        flagCz: Optional[str] = None,
        clearStatus: Optional[str] = None,
        trnsType: Optional[int] = None,
        seltType: Optional[str] = None,
        dataRange: Optional[str] = None,) -> dict:
    """
    结算信息
    #! 这个接口查找一家门店，不超过16行数据，就超过16秒，多家门店就报错，能用么？
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页码. Defaults to 1.
        size (int, optional): 每页数量. Defaults to 20.
        start_time (str, None): 结算日期区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        end_time (str, None): 结算日期区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
        certno (str, None): 证件号. Defaults to None.
        agnterName (str, None): 经办人姓名. Defaults to None.
        agnterCertno (str, None): 经办人证件号. Defaults to None.
        insutype (str, None): 险种类型. Defaults to None.
        orgcodg (list[str], None): 门店医保区化码. Defaults to None.
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
            - #! medical_insurance_Ent 中有想要的所有门店信息, 搞这么一出我是该说你脑残还是脑残

        psnName (str, None): 患者姓名. Defaults to None.
        setlIdBus (str, None): 订单号. Defaults to None.
        setlId (str, None): 结算ID. Defaults to None.
        mdtrtId (str, None): 就诊ID. Defaults to None.
        opterName (str, None): 收银员姓名. Defaults to None.
        clrOoptins (str, None): 经办机构. Defaults to None.
        medType (str, None): 医疗类别. Defaults to None.
            - 可在 medical_insurance_dict 中获取医疗类别, type=med_type 对应字段 value
        clrType (str, None): 清算类别. Defaults to None.
            - 可在 medical_insurance_dict 中获取清算类别, type=clr_type 对应字段 value
        psnCertType (str, None): 证件类型. Defaults to None.
            - 可在 medical_insurance_dict 中获取证件类型, type=psn_cert_type 对应字段 value
        mdtrtCertType (str, None): 凭证类型. Defaults to None.
            - 可在 medical_insurance_dict 中获取凭证类型, type=mdtrt_cert_type 对应字段 value
        diseCodg (str, None): 病种类型. Defaults to None.
            - #! 暂无数据，无法验证，界面上也找不到枚举值
        trnsState (str, None): 交易状态. Defaults to None.
            - 1-正常结算 2-正常退款 3-已补单
        flagCz (str, None): 冲正状态. Defaults to None.
            - 1-已冲正 0-未冲正
        clearStatus (str, None): 清算状态. Defaults to None.
            - W-未清算 Y-清算成功 N-清算失败 O-无需清算
        trnsType (int, None): 交易类型. Defaults to None.
            - 1-正常收费 2-异常收费 3-退费
        seltType (str, None): 结算类型. Defaults to None.
            - 1-省内异地 2-市本级 3-省外异地
        dataRange (str, None): 数据范围. Defaults to None.
            - 0-全部数据 1-退费不参与 2-全现金不参与

    Returns:
        dict: 结算信息
    """
    url = f"{base_url}/pageSummary"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if start_time:
        start_time = get_date_start_and_end_time(start_time)
    else:
        taday = get_current_date()
        start_time = get_date_start_and_end_time(taday)
    if end_time:
        end_time = get_date_start_and_end_time(end_time)
    else:
        taday = get_current_date()
        end_time = get_date_start_and_end_time(taday)

    payload = {
        "current": current,
        "size": size,
        "certno": certno,
        "agnterName": agnterName,
        "agnterCertno": agnterCertno,
        "insutype": insutype,
        "orgcodg": orgcodg,
        "startTime": start_time["start_time"] if start_time else None,
        "endTime": end_time["end_time"] if end_time else None,
        #! 下面这些参数，要搞两遍，意义何在？
        "psnName": psnName,
        "psn_name": psnName,
        "setlIdBus": setlIdBus,
        "setl_id_bus": setlIdBus,
        "setlId": setlId,
        "setl_id": setlId,
        "mdtrtId": mdtrtId,
        "mdtrt_id": mdtrtId,
        "opterName": opterName,
        "opter_name": opterName,
        "clrOoptins": clrOoptins,
        "clr_ooptins": clrOoptins,
        "medType": medType,
        "med_type": medType,
        "clrType": clrType,
        "clr_type": clrType,
        "psnCertType": psnCertType,
        "psn_cert_type": psnCertType,
        "mdtrtCertType": mdtrtCertType,
        "mdtrt_cert_type": mdtrtCertType,
        "diseCodg": diseCodg,
        "dise_codg": diseCodg,
        "trnsState": trnsState,
        "trns_state": trnsState,
        "flagCz": flagCz,
        "flag_cz": flagCz,
        "clearStatus": clearStatus,
        "clear_status": clearStatus,
        "trnsType": trnsType,
        "trns_type": trnsType,
        "seltType": seltType,
        "selt_type": seltType,
        "dataRange": dataRange,
        "data_range": dataRange,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def settlement_info_details(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        setlIdBus: Optional[str] = None,
        setlId: Optional[str] = None,
        psnNo: Optional[str] = None,
        certno: Optional[str] = None,
        medinsListCodg: Optional[str] = None,
        medinsListName: Optional[str] = None,
        medListCodg: Optional[str] = None,
        commonName: Optional[str] = None,
        orgcodg: Optional[List[str]] = None,
        medType: Optional[str] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,) -> dict:
    """
    医保结算明细-商品
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页码. Defaults to 1.
        size (int, optional): 每页数量. Defaults to 20.
        setlIdBus (str, None): 处方号. Defaults to None.
        setlId (str, None): 结算ID. Defaults to None.
        psnNo (str, None): 患者编号. Defaults to None.
        certno (str, None): 证件号. Defaults to None.
        medinsListCodg (str, None): 医保项目编码. Defaults to None.
        medinsListName (str, None): 医保项目名称. Defaults to None.
        medListCodg (str, None): 医保项目编码. Defaults to None.
        commonName (str, None): 商品名称. Defaults to None.
        orgcodg (list[str], None): 门店医保区化码. Defaults to None.
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        medType (str, None): 医疗类别. Defaults to None.
            - 可在 medical_insurance_dict 中获取医疗类别, type=med_type 对应字段 value
        startTime (str, None): 结算日期区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endTime (str, None): 结算日期区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    """
    url = f"{base_url}/getInventoryReportData"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startTime:
        startTime = get_date_start_and_end_time(startTime)
    else:
        taday = get_current_date()
        startTime = get_date_start_and_end_time(taday)
    if endTime:
        endTime = get_date_start_and_end_time(endTime)
    else:
        taday = get_current_date()
        endTime = get_date_start_and_end_time(taday)
    payload = {
        "current": current,
        "size": size,
        "setlIdBus": setlIdBus,
        "setlId": setlId,
        "psnNo": psnNo,
        "certno": certno,
        "medinsListCodg": medinsListCodg,
        "medinsListName": medinsListName,
        "medListCodg": medListCodg,
        "commonName": commonName,
        "orgcodg": orgcodg,
        "medType": medType,
        "startTime": startTime["start_time"] if startTime else None,
        "endTime": endTime["end_time"] if endTime else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def settlement_info_reconciliation(
        authorization: str,
        orgcodg: List[str],
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        stmtStatus: Optional[str] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,) -> dict:
    """
    医保对账记录
    Args:
        authorization (str): 认证信息
        orgcodg (list[str]): 门店医保区化码
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页码. Defaults to 1.
        size (int, optional): 每页数量. Defaults to 20.
        stmtStatus (str, None): 对账状态. Defaults to None.
            - Y-对账成功 N-对账失败 W-未对账
        startTime (str, None): 结算日期区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endTime (str, None): 结算日期区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    Returns:
        dict: 医保对账记录
    """
    url = f"{base_url}/getStmtData"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startTime:
        startTime = get_date_start_and_end_time(startTime)
    else:
        taday = get_current_date()
        startTime = get_date_start_and_end_time(taday)
    if endTime:
        endTime = get_date_start_and_end_time(endTime)
    else:
        taday = get_current_date()
        endTime = get_date_start_and_end_time(taday)
    payload = {
        "current": current,
        "size": size,
        "orgcodg": orgcodg,
        "stmtStatus": stmtStatus,
        "startTime": startTime["start_time"] if startTime else None,
        "endTime": endTime["end_time"] if endTime else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def settlement_info_liquidation(
        authorization: str,
        orgcodg: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        clearStatus: Optional[str] = None,
        startTime: Optional[str] = None,) -> dict:
    """
    医保清算记录查询
    Args:
        authorization (str): 认证信息
        orgcodg (str): 门店医保区化码
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页码. Defaults to 1.
        size (int, optional): 每页数量. Defaults to 20.
        clearStatus (str, None): 清算状态. Defaults to None.
            - Y-已清算 W-待清算
        startTime (str, None): 结算年月. Defaults to None.
            - 格式为: yyyy-MM
    Returns:
        dict: 医保清算记录查询
    """
    url = f"{base_url}/getClearData"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not startTime:
        taday = get_current_date()
        startTime = taday[:7]
    payload = {
        "current": current,
        "size": size,
        "orgcodg": orgcodg,
        "clearStatus": clearStatus,
        "startTime": startTime,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def mdtrt_cert_type_count(
        authorization: str,
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        mdtrtareaAdmvs: Optional[str] = None,
        startAge: Optional[int] = None,
        endAge: Optional[int] = None,
        trnsType: Optional[str] = None,
        orgcodg: Optional[List[str]] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,) -> dict:
    """
    医保就诊类型占比
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页码. Defaults to 1.
        size (int, optional): 每页数量. Defaults to 20.
        mdtrtareaAdmvs (str, None): 就诊地区划编码. Defaults to None.
            - #! 试了很多字段，最后也没搞明白填什么数据，后期验证
        startAge (int, None): 年龄范围区间-最小值. Defaults to None.
        endAge (int, None): 年龄范围区间-最大值. Defaults to None.
        trnsType (str, None): 交易类型. Defaults to None.
            - 1-收费 3-退费
        orgcodg (list[str], None): 门店医保区划码. Defaults to None.
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        startTime (str, None): 结算日期区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endTime (str, None): 结算日期区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    """
    url = f"{base_url}/queryMdtrtCertTypeCount"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if startTime:
        startTime = get_date_start_and_end_time(startTime)
    else:
        taday = get_current_date()
        startTime = get_date_start_and_end_time(taday)
    if endTime:
        endTime = get_date_start_and_end_time(endTime)
    else:
        taday = get_current_date()
        endTime = get_date_start_and_end_time(taday)
    payload = {
        "current": current,
        "size": size,
        "mdtrtareaAdmvs": mdtrtareaAdmvs,
        "startAge": startAge,
        "endAge": endAge,
        "trnsType": trnsType,
        "orgcodg": orgcodg,
        "startTime": startTime["start_time"] if startTime else None,
        "endTime": endTime["end_time"] if endTime else None,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def settlement_info_report(
        authorization: str,
        orgcodg: List[str],
        tenant_id: Optional[int] = None,
        current: int = 1,
        size: int = 20,
        clrType: Optional[str] = None,
        insutype: Optional[str] = None,
        medType: Optional[str] = None,
        seltTypeList: Optional[List[str]] = None,
        seltType: Optional[str] = None,
        dataRange: Optional[str] = None,
        data_type: Optional[int] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,) -> dict:
    """
    医保保障申报表
    Args:
        authorization (str): 认证信息
        orgcodg (list[str]): 门店医保区划码
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, optional): 当前页码. Defaults to 1.
        size (int, optional): 每页数量. Defaults to 20.
        clrType (str, None): 清算类别. Defaults to None.
            - 可在 medical_insurance_dict 中获取清算类别, type=clr_type 对应字段 value
        insutype (str, None): 险种类型. Defaults to None.
            - 可在 medical_insurance_dict 中获取险种类型, type=insutype 对应字段 value
        medType (str, None): 医疗类别. Defaults to None.
            - 可在 medical_insurance_dict 中获取医疗类别, type=med_type 对应字段 value
        #! 下面这两个参数有什么不同？难道多选就不能单选了，这是什么逻辑？
        seltTypeList (list[str], None): 结算类型. Defaults to None.
            - 1-省内异地 2-市本级 3-省外异地
        seltType (str, None): 结算类型. Defaults to None.
            - 1-省内异地 2-市本级 3-省外异地
        dataRange (str, None): 数据范围. Defaults to None.
            - 1-退费不参与 2-全现金不参与
        data_type (int, None): 申报类型. Defaults to None.
            - 6-按参保地区划申报
        startTime (str, None): 日期区间-开始. Defaults to None.
            - 格式为: yyyy-MM-dd
        endTime (str, None): 日期区间-结束. Defaults to None.
            - 格式为: yyyy-MM-dd
    """
    url = f"{base_url}/report"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    taday = get_current_date()

    payload = {
        "current": current,
        "size": size,
        "orgcodg": orgcodg,
        "clrType": clrType,
        "insutype": insutype,
        "medType": medType,
        "seltTypeList": seltTypeList,
        "seltType": seltType,
        "dataRange": dataRange,
        "type": data_type,
        "startTime": startTime if startTime else taday,
        "endTime": endTime if endTime else taday,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()


async def report_list_by_user_type(
        authorization: str,
        tenant_id: Optional[int] = None,
        orgcodg: Optional[List[str]] = None,
        psnType: Optional[str] = None,
        declareMon: Optional[str] = None, ) -> dict:
    """
    按人员类型申报
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        orgcodg (list[str], None): 门店医保区划码. Defaults to None.
            - 可在 common_organ_of_login_page_of_status 中获取门店 code , 然后在 medical_insurance_ent 中获取 nationalMiCode 字段
        psnType (str, None): 人员类别. Defaults to None.
            - 可在 medical_insurance_dict 中获取人员类别, type=psn_type 对应字段 value
        declareMon (str, None): 结算月份. Defaults to None.
            - 格式为: yyyy-MM
    """
    url = f"{base_url}/reportListByUserType"
    headers = {
        "Authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    if not declareMon:
        taday = get_current_date()
        declareMon = taday[:7]

    payload = {
        "orgcodg": orgcodg,
        "psnType": psnType,
        "declareMon": declareMon,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
