"""
企业微信API
"""

from api.qy_weixin.http_api.access_token import get_access_token
from api.qy_weixin.http_api.department import (
    department_info, department_list, department_simplelist)
from api.qy_weixin.http_api.meeting import (
    meeting_cancel, meeting_info, user_meeting_list, create_meeting, update_meeting, meeting_statistics)
from api.qy_weixin.http_api.oa import (
    add_calendar,
    del_calendar,
    get_calendar,
    update_calendar,
    approval_template_detail,
    approval_detail,
    applyevent,
)
from api.qy_weixin.http_api.user import (
    get_user_info,
    department_user_simplelist,
    department_user_list,
    convert_to_openid,
    userid_by_mobile,
    userid_by_email,
)
from api.qy_weixin.http_api.wedoc import (
    create_doc,
)
from api.qy_weixin.http_api.wedrive import (
    space_create,
    space_dismiss,
)

__all__ = [
    "get_access_token",
    "department_info",
    "department_list",
    "department_simplelist",
    "meeting_cancel",
    "meeting_info",
    "user_meeting_list",
    "create_meeting",
    "update_meeting",
    "meeting_statistics",
    "add_calendar",
    "del_calendar",
    "get_calendar",
    "update_calendar",
    "approval_template_detail",
    "approval_detail",
    "applyevent",
    "get_user_info",
    "department_user_simplelist",
    "department_user_list",
    "convert_to_openid",
    "userid_by_mobile",
    "userid_by_email",
    "create_doc",
    "space_create",
    "space_dismiss"
]
