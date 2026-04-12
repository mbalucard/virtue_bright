"""
会员用户
    - 会员卡开卡渠道列表-下拉检索用: member_channel
    - 会员列表: member_user_list
"""

from httpx import AsyncClient
from typing import Optional

from configs.api_configes import yaoud_env
from api.yaoud_api.general_tools import get_date_start_and_end_time, timestamp


base_url = f"{yaoud_env['url']}/cdp/memberUser"
TTL = yaoud_env["timeout"]


async def member_channel(
        authorization: str,
        tenant_id: Optional[int] = None,) -> dict:
    """
    会员卡开卡渠道列表-下拉检索用
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
    Returns:
        dict: 会员卡开卡渠道列表
    """
    url = f"{base_url}/queryMemberChannelList"
    headers = {
        "authorization": authorization,
        "client-tom": "Y",
        "tenant-id": str(tenant_id) if tenant_id else "",
    }
    params = {
        "_": timestamp(),
    }
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=TTL)
    return response.json()


async def member_user_list(
    authorization: str,
    tenant_id: Optional[int] = None,
    current: Optional[int] = 1,
    size: Optional[int] = 10,
    groupId: Optional[int] = None,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    telephone: Optional[str] = None,
    cardCode: Optional[str] = None,
    identityCard: Optional[str] = None,
    # 字典列表参数
    channelCodeList: Optional[dict[str, str]] = None,
    cardStoreList: Optional[dict[str, str]] = None,
    gradeList: Optional[dict[str, str]] = None,
    # ID+Label参数
    sex: Optional[int] = None,
    sexLabel: Optional[str] = None,
    bindWechatCp: Optional[int] = None,
    bindWechatCpLabel: Optional[str] = None,
    status: Optional[int] = None,
    statusDesc: Optional[str] = None,
    ownerEmpId: Optional[int] = None,
    ownerEmpName: Optional[str] = None,
    labelId: Optional[int] = None,
    labelName: Optional[str] = None,
    # 区间类参数
    birthdayBegin: Optional[str] = None,
    birthdayEnd: Optional[str] = None,
    ageBegin: Optional[str] = None,
    ageEnd: Optional[str] = None,
    pointBegin: Optional[str] = None,
    pointEnd: Optional[str] = None,
    accountBegin: Optional[str] = None,
    accountEnd: Optional[str] = None,
    registerTimeBegin: Optional[str] = None,
    registerTimeEnd: Optional[str] = None,
    cardTimeBegin: Optional[str] = None,
    cardTimeEnd: Optional[str] = None,
    growthBegin: Optional[str] = None,
        growthEnd: Optional[str] = None,) -> dict:
    """
    会员列表
    Args:
        authorization (str): 认证信息
        tenant_id (int, None): 租户ID. Defaults to None.
        current (int, None): 当前页. Defaults to 1.
        size (int, None): 每页数量. Defaults to 10.
        groupId (int, None): 会员权益组id, Defaults to None.
            -可在get_member_group_list中获取.
        name (str, None): 会员姓名. Defaults to None.
        phone (str, None): 会员手机号. Defaults to None.
        telephone (str, None): 会员固话. Defaults to None.
        cardCode (str, None): 会员卡号. Defaults to None.
        identityCard (str, None): 会员身份证号. Defaults to None.
        channelCodeList (dict[str, str], None): 会员卡开卡渠道列表.Defaults to None.
            - 可在 member_channel 中找到。{code: "ERP", name: "ERP"} 
        cardStoreList (dict[str, str], None): 会员卡门店列表.Defaults to None.
            - 可在 get_stores 中找到。{id: "id", name: "shortName"} 
        gradeList (dict[str, str], None): 会员等级列表.Defaults to None.
            - 可在 get_grade_by_group_id 中找到。{id: "id", name: "name"} 
        sex (int, None): 会员性别ID. Defaults to None.
            - (1男,2女,3其它)
        sexLabel (str, None): 会员性别标签. Defaults to None.
        bindWechatCp (int, None): 是否绑定企业微信. Defaults to None.
            - (1是,0否)
        bindWechatCpLabel (str, None): 是否绑定企业微信标签. Defaults to None.
        status (int, None): 会员状态ID. Defaults to None.
            - (1:有效,5:冻结，10:注销中，15:已注销)
        statusDesc (str, None): 会员状态标签. Defaults to None.
        ownerEmpId (int, None): 归属员工ID. Defaults to None.
        ownerEmpName (str, None): 归属员工姓名. Defaults to None.
        labelId (int, None): 会员标签. Defaults to None.
            - 可在 item_list 中获取ID
        labelName (str, None): 会员标签名称. Defaults to None.
            - 可在 item_list 中获取名称
        birthdayBegin (str, None): 会员生日区间-开始时间. Defaults to None.
            - 日期格式 mm-dd
        birthdayEnd (str, None): 会员生日区间-结束时间. Defaults to None.
            - 日期格式 mm-dd
        ageBegin (str, None): 会员年龄区间-开始. Defaults to None.
        ageEnd (str, None): 会员年龄区间-结束. Defaults to None.
        pointBegin (str, None): 会员积分区间-开始. Defaults to None.
        pointEnd (str, None): 会员积分区间-结束. Defaults to None.
        accountBegin (str, None): 会员账户余额区间-开始. Defaults to None.
        accountEnd (str, None): 会员账户余额区间-结束. Defaults to None.
        registerTimeBegin (str, None): 会员注册时间区间-开始. Defaults to None.
            - 日期格式 yyyy-mm-dd
        registerTimeEnd (str, None): 会员注册时间区间-结束. Defaults to None.
            - 日期格式 yyyy-mm-dd
        cardTimeBegin (str, None): 会员开卡时间区间-开始. Defaults to None.
            - 日期格式 yyyy-mm-dd
        cardTimeEnd (str, None): 会员开卡时间区间-结束. Defaults to None.
            - 日期格式 yyyy-mm-dd
        growthBegin (str, None): 会员成长值区间-开始. Defaults to None.
            - 日期格式 yyyy-mm-dd
        growthEnd (str, None): 会员成长值区间-结束. Defaults to None.
            - 日期格式 yyyy-mm-dd
    Returns:
        dict: 会员列表
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
        "groupId": groupId,
        "name": name,
        "phone": phone,
        "telephone": telephone,
        "cardCode": cardCode,
        "identityCard": identityCard,
        #! 哪个傻逼写的，直接给字典列表
        "channelCodeList": channelCodeList,
        "cardStoreList": cardStoreList,
        "gradeList": gradeList,
        #! 给ID还要给标签，脑子然雷打了
        "sex": sex,
        "sexLabel": sexLabel,
        "bindWechatCp": bindWechatCp,
        "bindWechatCpLabel": bindWechatCpLabel,
        "status": status,
        "statusDesc": statusDesc,
        "ownerEmpId": ownerEmpId,
        "ownerEmpName": ownerEmpName,
        "labelId": labelId,
        "labelName": labelName,
        #! 年龄、积分、账户余额、成长值，给字符串，你他妈会不会
        "birthdayBegin": birthdayBegin,
        "birthdayEnd": birthdayEnd,
        "ageBegin": ageBegin,
        "ageEnd": ageEnd,
        "pointBegin": pointBegin,
        "pointEnd": pointEnd,
        "accountBegin": accountBegin,
        "accountEnd": accountEnd,
        "registerTimeBegin": registerTimeBegin,
        "registerTimeEnd": registerTimeEnd,
        "cardTimeBegin": cardTimeBegin,
        "cardTimeEnd": cardTimeEnd,
        "growthBegin": growthBegin,
        "growthEnd": growthEnd,
    }
    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=TTL)
    return response.json()
