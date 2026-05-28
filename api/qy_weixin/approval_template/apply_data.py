"""
审批申请数据模版
    - 请假申请数据模版 leave_apply_data
"""

from api.qy_weixin.http_api.oa import approval_template_detail
from api.qy_weixin.http_api.general_tools import get_second


async def leave_apply_data(
    access_token: str,
    leave_type: int,
    begin_time: str,
    close_time: str,
    reason_leave: str,):
    """
    请假申请数据模版
    Args:
        access_token (str): 企业微信access_token
        leave_type (int): 请假类型
            - 1: 年假 2: 事假 3: 病假 4: 调休假 5: 婚假 6: 产假 7: 陪产假 8: 育儿假
        begin_time (str): 请假开始时间
            - 格式: YYYY-MM-DD HH:MM
        close_time (str): 请假结束时间
            - 格式: YYYY-MM-DD HH:MM
        reason_leave (str): 请假原因
    Returns:
        dict: 请假申请数据模版
    """
    template_id = "C4c73p9SyuauXqWVSmiGGrSLNzG3MmgJ6BuBxmZAT"
    response = await approval_template_detail(access_token, template_id)
    if response.get('errcode') != 0:
        raise Exception(response['errmsg'])
    controls = response.get('template_content', {}).get('controls', [])
    item_dict = {item['id']: item['name']
                 for item in response.get('vacation_list', {}).get('item', [])}
    start_time = get_second(begin_time)
    end_time = get_second(close_time)

    apply_data = {
        "contents": [
            {
                "control": controls[0].get('property').get("control"),
                "id": controls[0].get('property').get("id"),
                "title": controls[0].get('property').get("title"),
                "value": {
                    "vacation": {
                        "selector": {
                            "type": "single",
                            "options": [
                                {
                                    "key": str(leave_type),
                                    "value": item_dict.get(leave_type)
                                }
                            ]
                        },
                        "attendance": {
                            "date_range": {
                                "type": "hour",
                                "new_begin": start_time,
                                "new_end": end_time,
                                "new_duration": end_time - start_time
                            },
                        },
                    },
                },
            },
            {
                "control": controls[1].get('property').get("control"),
                "id": controls[1].get('property').get("id"),
                "title": controls[1].get('property').get("title"),
                "value": {"text": reason_leave}
            }
        ]
    }
    return apply_data


if __name__ == '__main__':
    import asyncio
    from api.qy_weixin.http_api.access_token import get_access_token

    auth = get_access_token()

    async def main():
        apply_data = await leave_apply_data(
            access_token=auth['access_token'],
            leave_type=4,
            begin_time="2023-01-01 09:00",
            close_time="2023-01-01 10:00",
            reason_leave="测试"
        )
        print(apply_data)

    asyncio.run(main())
