"""
OA接口
    - 添加日历 add_calendar
    - 删除日历 delete_calendar
    - 获取日历 get_calendar
    - 更新日历 update_calendar
    - 获取审批模板详情 approval_template_detail
    - 获取审批申请详情 approval_detail
    - 提交审批申请 applyevent
"""

from configs.api_configes import qy_env
from httpx import AsyncClient
from typing import Optional, List

base_url = f"{qy_env['base_url']}/oa"
ttl = qy_env["ttl"]


async def add_calendar(
        access_token: str,
        summary: str,
        color: str = "#FF3030",
        description: Optional[str] = None,
        admins: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        permission: int = 1,
        is_public: int = 0,
        partyids: Optional[List[int]] = None,
        set_as_default: int = 0,
        is_corp_calendar: int = 0,) -> dict:
    """
    添加日历
    文档: https://developer.work.weixin.qq.com/document/path/93647
    Args:
        access_token: 企业应用的access_token
        summary(str): 日历标题
        color(str): 日历颜色 Default: "#FF3030"
            - 颜色值为RGB颜色编码16进制表示
        description(str,None): 日历描述 Default: None
            - 长度不能超过512个字符
        admins(list[str],None): 日历管理员用户ID列表, Default: None
            - 最多指定3人
        userids(list[str],None): 日历通知范围成员用户ID列表, Default: None
            - 最多指定1000人
        permission(int): 日历通知范围成员权限 Default: 1
            - 1-查看 3-仅查看闲忙状态
        is_public(int): 是否公共日历 Default: 0
            - 0-否 1-是
            - 每个人最多可创建或订阅100个公共日历
            - 该属性不可更新
        partyids(list[int],None): 日历公开范围部门ID列表, Default: None
            - 最多指定100个部门
        set_as_default(int): 是否将该日历设置为access_token所对应应用的默认日历 Default: 0
            - 0-否 1-是
            - 第三方应用不支持使用该参数
        is_corp_calendar(int): 是否为企业日历 Default: 0
            - 0-否 1-是
            - 每个企业最多可创建20个全员日历
            - 全员日历也是公共日历的一种，需要指定public_range
            - 全员日历不支持指定颜色、默认日历、只读权限
            - 该属性不可更新
    Returns:
        dict: 包含日历ID(cal_id)的字典
    """
    url = f"{base_url}/calendar/add"
    params = {
        "access_token": access_token,
    }
    # 日历通知范围成员列表
    shares = []
    if admins:
        shares = [{"userid": admin, "permission": permission}
                  for admin in admins]
    if userids:
        users_shares = [{"userid": userid, "permission": permission}
                        for userid in userids]
        shares.extend(users_shares)
    # 公开范围
    if is_public:
        users = admins.copy() if admins else []
        if userids:
            users.extend(userids)
        public_range = {"userids": users}
        if partyids:
            public_range["partyids"] = partyids

    if is_corp_calendar:
        if not public_range:
            raise ValueError("is_corp_calendar must specify public_range")

    payload = {
        "calendar": {
            "summary": summary,
            "color": color,
            "description": description,
            "admins": admins,
            "shares": shares if shares else None,
            "is_public": is_public,
            "public_range": public_range if is_public else None,
            "set_as_default": set_as_default,
            "is_corp_calendar": is_corp_calendar,
        },
        "agent_id": qy_env["agent_id"],
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()


async def del_calendar(access_token: str, cal_id: str) -> dict:
    """
    删除日历
    文档: https://developer.work.weixin.qq.com/document/path/97718
    Args:
        access_token: 企业应用的access_token
        cal_id(str): 日历ID
    Returns:
        dict: 包含删除结果的字典
    """
    url = f"{base_url}/calendar/del"
    params = {
        "access_token": access_token,
    }
    payload = {
        "cal_id": cal_id,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()


async def get_calendar(access_token: str, cal_id_list: List[str]) -> dict:
    """
    获取日历
    文档: https://developer.work.weixin.qq.com/document/path/97717
    Args:
        access_token: 企业应用的access_token
        cal_id_list(list[str]): 日历ID列表
    Returns:
        dict: 日历详情
    """
    url = f"{base_url}/calendar/get"
    params = {
        "access_token": access_token,
    }
    payload = {
        "cal_id_list": cal_id_list,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()


async def update_calendar(
        access_token: str,
        cal_id: str,
        summary: str,
        color: str = "#FF3030",
        description: Optional[str] = None,
        skip_public_range: int = 0,
        admins: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        permission: int = 1,
        partyids: Optional[List[int]] = None,) -> dict:
    """
    更新日历
    文档: https://developer.work.weixin.qq.com/document/path/97716
    Args:
        access_token: 企业应用的access_token
        cal_id(str): 日历ID
        summary(str): 日历标题
        color(str): 日历颜色 Default: "#FF3030"
            - RGB颜色编码16进制表示
        description(str,None): 日历描述 Default: None
        skip_public_range(int): 是否不更新可订阅范围 Default: 0 会更新可订阅范围
            - 0-否 1-是
        admins(list[str],None): 日历管理员用户ID列表, Default: None
            - 最多指定3人
        userids(list[str],None): 日历通知范围成员用户ID列表, Default: None
            - 最多指定1000人
        permission(int): 日历通知范围成员权限 Default: 1
            - 1-查看 3-仅查看闲忙状态
        partyids(list[int],None): 公开给指定部门ID列表, Default: None
            - 最多指定100个部门
    Returns:
        dict: 包含更新结果的字典
    """
    calendar_json = await get_calendar(access_token, [cal_id])
    if calendar_json["errcode"] != 0:
        return calendar_json

    url = f"{base_url}/calendar/update"
    params = {
        "access_token": access_token,
    }
    # 日历通知范围成员列表
    shares = []
    if admins:
        shares = [{"userid": admin, "permission": permission}
                  for admin in admins]
    if userids:
        users_shares = [{"userid": userid, "permission": permission}
                        for userid in userids]
        shares.extend(users_shares)

    # 公开范围
    if calendar_json['calendar_list'][0]['is_public']:
        public_range = {}
        users = admins.copy() if admins else []
        if userids:
            users.extend(userids)
        public_range["userids"] = users
        if partyids:
            public_range["partyids"] = partyids
    else:
        public_range = None

    payload = {
        "skip_public_range": skip_public_range,
        "calendar": {
            "cal_id": cal_id,
            "admins": admins,
            "summary": summary,
            "color": color,
            "description": description,
            "shares": shares if shares else None,
            "public_range": public_range,
        },
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()


async def approval_template_detail(
    access_token: str,
    template_id: str,) -> dict:
    """
    获取审批模板详情
    文档: https://developer.work.weixin.qq.com/document/path/91982
    Args:
        access_token: 企业应用的access_token
        template_id: 审批模板ID
    Returns:
        dict: 审批模板详情
    """
    url = f"{base_url}/gettemplatedetail"
    params = {"access_token": access_token}
    payload = {"template_id": template_id}
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()


async def approval_detail(
    access_token: str,
    sp_no: str,) -> dict:
    """
        获取审批申请详情
        文档: https://developer.work.weixin.qq.com/document/path/92634
        Args:
            access_token: 企业应用的access_token
            sp_no: 审批申请编号
        Returns:
            dict: 审批申请详情
    """
    url = f"{base_url}/getapprovaldetail"
    params = {"access_token": access_token}
    payload = {"sp_no": sp_no}
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()



async def applyevent(
    access_token: str,
    template_id: str,
    user_id: str,
    apply_data: dict,
    use_template_approver: int = 1,
    choose_department: Optional[int] = None,
    process: Optional[dict] = None,
    summary_list: Optional[List[dict]] = None,)->dict:
    """
    提交审批申请
    文档: https://developer.work.weixin.qq.com/document/path/91853
    Args:
        access_token: 企业应用的access_token
        template_id: 审批模板ID
        user_id: 创建人userid
        apply_data: 审批申请数据
        use_template_approver: 审批人模式 Default: 1
            - 0-通过接口指定审批人、抄送人 1-使用此模板在管理后台设置的审批流程
            - 如果为0，必填process
        choose_department: 提单者提单部门id Default: None
            - None-默认主部门
        process: 审批流程 Default: None
        summary_list: 摘要信息列表,用于显示在审批通知卡片 Default: None
            - list中最多指定3条摘要      
    """
    url = f"{base_url}/applyevent"
    params = {"access_token": access_token}
    payload = {
        "creator_userid": user_id,  
        "template_id": template_id,
        "use_template_approver": use_template_approver,
        "choose_department": choose_department,
        "process": process,
        "apply_data": apply_data,
        "summary_list": summary_list,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
    return response.json()



if __name__ == "__main__":
    import asyncio
    from access_token import get_access_token
    # wcsBwaDgAA-6XqTQspufa-7vHTPcp9hA
    auth = get_access_token()
    template_id = "C4c73p9SyuauXqWVSmiGGrSLNzG3MmgJ6BuBxmZAT"
    sp_no = "202604280040"
    
    async def main():
        access_token = auth["access_token"]
        
        data = await approval_detail(access_token, sp_no)
        print(data)

    data = asyncio.run(main())
    print(data)
