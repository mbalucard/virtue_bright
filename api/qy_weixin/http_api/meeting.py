"""
会议接口
    - 取消会议 meeting_cancel
    - 获取会议详情 meeting_info
    - 获取成员会议ID列表 user_meeting_list
    - 获取会议列表 meeting_list
    - 创建会议 create_meeting
    - 更新会议 update_meeting
"""

from api.qy_weixin.http_api.general_tools import timestamp, get_current_date, get_second
from config.request_config import qy_env
from httpx import AsyncClient
from typing import Optional, List

base_url = f"{qy_env['base_url']}/meeting"
agent_id = qy_env['agent_id']
ttl = qy_env["ttl"]


async def meeting_cancel(
        access_token: str,
        meeting_id: str) -> dict:
    """
    取消会议
    文档: https://developer.work.weixin.qq.com/document/path/99048
    Args:
        access_token (str): 企业微信 access_token
        meeting_id (str): 会议ID
    Returns:
        取消会议结果
    """
    url = f"{base_url}/cancel"
    params = {"access_token": access_token, }
    payload = {"meetingid": meeting_id}
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
    return response.json()


async def meeting_info(
        access_token: str,
        meeting_id: str) -> dict:
    """
    获取会议详情
    文档: https://developer.work.weixin.qq.com/document/path/99049
    Args:
        access_token (str): 企业微信 access_token
        meeting_id (str): 会议ID
    Returns:
        会议详情
    """
    url = f"{base_url}/get_info"
    params = {"access_token": access_token, }
    payload = {"meetingid": meeting_id}
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
    return response.json()


async def user_meeting_list(
        access_token: str,
        user_id: str,
        begin_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 20,
        cursor: Optional[str] = None) -> dict:
    """
    获取成员会议ID列表
    文档: https://developer.work.weixin.qq.com/document/path/99050
    Args:
        access_token (str): 企业微信 access_token
        user_id (str): 用户ID
        begin_time (str,None): 查询时间区间-开始时间
            - 格式为YYYY-MM-DD HH:MM
        end_time (str,None): 查询时间区间-结束时间
            - 格式为YYYY-MM-DD HH:MM
        limit (int): 每页返回的最大会议数量,默认值为None.
            - 最大为100
        cursor (str,None): 分页游标,默认值为None.
            - None: 获取第一页
            - 该参数游上一次返回
    Returns:
        成员会议ID列表
    """
    url = f"{base_url}/get_user_meetingid"
    params = {"access_token": access_token, }

    if begin_time:
        begin_time = get_second(begin_time)
    if end_time:
        end_time = get_second(end_time)

    payload = {
        "userid": user_id,
        "begin_time": begin_time,
        "end_time": end_time,
        "limit": limit,
        "cursor": cursor
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
    return response.json()


async def create_meeting(
        access_token: str,
        admin_userid: str,
        title: str,
        meeting_start: str,
        meeting_duration: int = 30,
        description: Optional[str] = None,
        location: Optional[str] = None,
        agentid: str = agent_id,
        calendar_id: Optional[str] = None,
        user_ids: List[str] = [],
        remind_scope: int = 1,
        password: Optional[int] = None,
        enable_waiting_room: bool = False,
        allow_enter_before_host: bool = True,
        enable_enter_mute: int = 1,
        enable_screen_watermark: bool = False,
        host_userids: List[str] = [],
        ring_userids: List[str] = [],
        is_repeat: int = 0,
        repeat_type: int = 1,
        repeat_until: Optional[int] = None,
        repeat_interval: int = None,
        remind_before: List[int] = [0]) -> dict:
    """
    创建会议
    文档: https://developer.work.weixin.qq.com/document/path/99104
    Args:
        access_token (str): 企业微信 access_token
        admin_userid (str): 会议组织者用户ID
        title (str): 会议标题
            - 最大40个字节
        meeting_start (str): 会议开始时间
            - 格式为YYYY-MM-DD HH:MM
        meeting_duration (int): 会议时长 Default: 30
            - 单位为分钟
            - 非会员最大40分钟
        description (str,None): 会议描述 Default: None
            - 最多支持500个字节
        location (str,None): 会议地点 Default: None
            - 最大128个字节
        agentid (str): 应用ID Default: QYAPI_AGENT_ID
        calendar_id (str,None): 日历ID Default: None
        user_ids (List[str]): 会议参与用户ID列表 Default: []
            - 普通用户最多100人
            - 会员最多300人
        remind_scope (int): 会议开始时来电提醒方式 Default: 1
            - 1: 不提醒 2: 仅提醒主持人 3: 提醒所有成员入 4: 指定部分人响铃
        password (int,None): 会议密码 Default: None
            - 仅可输入4-6位纯数字
        enable_waiting_room (bool): 是否开启等待室 Default: False
        allow_enter_before_host (bool): 是否允许参会者在主持人加入前进入 Default: True
        enable_enter_mute (int): 是否开启入会静音 Default: 1
            - 0: 不开启 1: 开启 2: 超过6人后自动开启静音
        enable_screen_watermark (bool): 是否开启屏幕水印 Default: False
        host_userids (List[str]): 会议主持人用户ID列表 Default: []
            - 最多10人
            - 高级会员可用
        ring_userids (List[str]): 会议响铃用户ID列表 Default: []
            - 仅在remind_scope为4时有效
            - 如果remind_scope为4，但是ring_userids为空，则全部成员均不响铃
        is_repeat (int): 是否是周期性会议 Default: 0
            - 0: 否 1: 是
        repeat_type (int): 周期性会议重复类型 Default: 1
            - 0.每天；1.每周；2.每月；7.每个工作日
        repeat_until (int,None): 重复结束日期 Default: None
            - 格式为YYYY-MM-DD
            - 每天\每个工作日\每周 最多重复200次会议
            - 每两周\每月最多重复50次会议
        repeat_interval (int): 重复间隔 Default: 1
            - 当repeat_type为1时生效,且值不能大于2
        remind_before (List[int]): 会议开始前提醒时间 Default: [0]
            - 单位为分钟
            - 默认会议开始时提醒 可选值 5,15,60,1440
    """
    url = f"{base_url}/create"
    params = {"access_token": access_token, }
    # 会议配置参数
    settings = {
        "remind_scope": remind_scope,
        "password": password if len(str(password)) in range(4, 7) else None,
        "enable_waiting_room": enable_waiting_room,
        "allow_enter_before_host": allow_enter_before_host,
        "enable_enter_mute": enable_enter_mute,
        "enable_screen_watermark": enable_screen_watermark,
        "hosts": {"userid": host_userids},
        "ring_users": {"userid": ring_userids} if remind_scope == 4 else None,
    }

    # 重复会议参数
    if is_repeat:
        if repeat_until:
            repeat_until = get_second(f"{repeat_until} 23:59")
        remind_before = [i * 60 for i in remind_before]
        reminders = {
            "is_repeat": is_repeat,
            "repeat_type": repeat_type,
            "repeat_until": repeat_until,
            "repeat_interval": repeat_interval if repeat_type == 1 and repeat_interval <= 2 else None,
            "remind_before": remind_before,
        }
    else:
        reminders = None

    # 会议请求主体参数
    if meeting_start:
        meeting_start = get_second(meeting_start)
    meeting_duration = meeting_duration * 60
    if admin_userid not in user_ids:
        user_ids.append(admin_userid)

    payload = {
        "admin_userid": admin_userid,
        "title": title,
        "meeting_start": meeting_start,
        "meeting_duration": meeting_duration,
        "description": description,
        "location": location,
        "agentid": agentid,
        "calendar_id": calendar_id,
        "invitees": {"userid": user_ids},
        "settings": settings,
        "reminders": reminders,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
    return response.json()


async def update_meeting(
        access_token: str,
        meeting_id: str,
        title: str = None,
        meeting_start: Optional[int] = None,
        meeting_duration: Optional[int] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        calendar_id: Optional[str] = None,
        user_ids: Optional[List[str]] = None,
        remind_scope: Optional[int] = None,
        password: Optional[int] = None,
        enable_waiting_room: Optional[bool] = None,
        allow_enter_before_host: Optional[bool] = None,
        enable_enter_mute: Optional[int] = None,
        enable_screen_watermark: Optional[bool] = None,
        host_userids: Optional[List[str]] = None,
        ring_userids: Optional[List[str]] = None,
        is_repeat: Optional[int] = None,
        repeat_type: Optional[int] = None,
        repeat_until: Optional[str] = None,
        repeat_interval: Optional[int] = None,
        remind_before: Optional[List[int]] = None,) -> dict:
    """
    更新会议
    文档: https://developer.work.weixin.qq.com/document/path/99047

    Args:
        access_token (str): 企业微信access_token
        meeting_id (str): 会议id
        title (str,None): 会议标题 Default: None
        meeting_start (int,None): 会议开始时间 Default: None
            - 格式为YYYY-MM-DD HH:mm
            - 会议开始时间必须在当前时间之后
            - 必须同时提供 meeting_duration 否则将不会更改该参数
        meeting_duration (int,None): 会议时长 Default: None
            - 单位为分钟
            - 必须同时提供 meeting_start 否则将不会更改该参数
        description (str,None): 会议描述 Default: None
        location (str,None): 会议地点 Default: None
        calendar_id (str,None): 会议所属日历ID Default: None
        user_ids (List[str],None): 参会成员列表 Default: None
        remind_scope (int,None): 会议开始时来电提醒方式 Default: None
            - 1: 不提醒 2: 仅提醒主持人 3: 提醒所有成员入 4: 指定部分人响铃
        password (int,None): 入会密码 Default: None
            - 4-6位数字密码
        enable_waiting_room (bool,None): 是否开启等候室 Default: None
        allow_enter_before_host (bool,None): 是否允许成员在主持人进会前加入 Default: None
        enable_enter_mute (int,None): 成员入会时静音 Default: None
            - 0: 不开启 1: 开启 2: 超过6人后自动开启静音
        enable_screen_watermark (bool,None): 是否开启屏幕水印 Default: None
        host_userids (List[str],None): 会议主持人人列表 Default: None
            - 最多10人
            - 高级会员可用
        ring_userids (List[str],None): 指定响铃的成员列表 Default: None
            - 仅在remind_scope为4时有效
            - 如果remind_scope为4，但是ring_userids为空，则全部成员均不响铃
        is_repeat (int): 是否是周期性会议 Default: None
            - 0: 否 1: 是
        repeat_type (int,None): 周期性会议重复类型 Default: None
            - 0.每天；1.每周；2.每月；7.每个工作日
        repeat_until (int,None): 重复结束日期 Default: None
            - 格式为YYYY-MM-DD
            - 每天\每个工作日\每周 最多重复200次会议
            - 每两周\每月最多重复50次会议
        repeat_interval (int,None): 重复间隔 Default: None
            - 当repeat_type为1时生效,且值不能大于2
        remind_before (List[int],None): 会议开始前提醒时间 Default: None
            - 单位为分钟
            - 默认会议开始时提醒 可选值 5,15,60,1440

    Returns:
        dict: 会议信息
    """
    url = f"{base_url}/update"
    params = {"access_token": access_token, }

    # 会议配置参数
    settings = {
        "remind_scope": remind_scope,
        "password": password if len(str(password)) in range(4, 7) else None,
        "enable_waiting_room": enable_waiting_room,
        "allow_enter_before_host": allow_enter_before_host,
        "enable_enter_mute": enable_enter_mute,
        "enable_screen_watermark": enable_screen_watermark,
        "hosts": {"userid": host_userids} if host_userids else None,
        "ring_users": {"userid": ring_userids} if remind_scope == 4 and ring_userids else None,
    }

    # 重复会议参数
    if is_repeat:
        if repeat_until:
            repeat_until = get_second(f"{repeat_until} 23:59")
        remind_before = [i * 60 for i in remind_before]
        reminders = {
            "is_repeat": is_repeat,
            "repeat_type": repeat_type,
            "repeat_until": repeat_until,
            "repeat_interval": repeat_interval if repeat_type == 1 and repeat_interval <= 2 else None,
            "remind_before": remind_before,
        }
    else:
        reminders = None

    # 会议主参数
    if meeting_start and meeting_duration:
        meeting_start = get_second(meeting_start)
        meeting_duration = meeting_duration * 60
    else:
        meeting_start = None
        meeting_duration = None
    payload = {
        "meetingid": meeting_id,
        "title": title,
        "meeting_start": meeting_start,
        "meeting_duration": meeting_duration,
        "description": description,
        "location": location,
        "calendar_id": calendar_id,
        "invitees": {"userid": user_ids} if user_ids else None,
        "settings": settings,
        "reminders": reminders,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
    return response.json()


async def meeting_statistics(
        access_token: str,
        begin_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 200,
        cursor: Optional[str] = None,
        meeting_type: int = 1,) -> dict:
    """
    获取会议统计数据
    文档: https://developer.work.weixin.qq.com/document/path/99651
    Args:
        access_token (str): 企业微信access_token
        begin_time (Optional[str], None): 开始时间 Default: None
            - 格式为YYYY-MM-DD HH:mm
        end_time (Optional[str], None): 结束时间 Default: None
            - 格式为YYYY-MM-DD HH:mm
        limit (int, 100): 每页数量 Default: 200
            - 最多1000条
        cursor (Optional[str], None): 分页游标 Default: None
            - 由上一次调用返回，首次调用可不填
        meeting_type (int, 1): 会议类型 Default: 1
            - 1: 发起成功的会议记录
            - 2: 发起失败的会议
    """
    url = f"{base_url}/statistics/get_start_list"
    params = {"access_token": access_token}

    if begin_time:
        begin_time = get_second(begin_time)
    if end_time:
        end_time = get_second(end_time)

    payload = {
        "begin_time": begin_time,
        "end_time": end_time,
        "limit": limit,
        "cursor": cursor,
        "type": meeting_type,
    }
    async with AsyncClient() as client:
        response = await client.post(url, params=params, json=payload, timeout=ttl)
        response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    import asyncio
    from access_token import get_access_token

    meeting_id = "hysBwaDgAADnjOCI8edho3ku5PESGIqA"
    async def main():
        auth = get_access_token()
        access_token = auth["access_token"]
        data = await meeting_info(
            access_token=access_token,
            meeting_id=meeting_id,
        )
        print(data)

    asyncio.run(main())
