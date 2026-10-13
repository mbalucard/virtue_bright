from utils.db_link import db_server
from configs.server import DockerPostgreSQL
from api.qy_weixin.http_api.access_token import get_access_token
from api.qy_weixin.http_api.user import department_user_list
from api.qy_weixin.data_manipulation.models import QyWeixinDepartment, QyWeixinUser, QyWeixinUserDepartment

from sqlalchemy import select
from sqlalchemy.orm.session import Session
from typing import Literal, Sequence, Any, Optional, List, Set


def get_id_list(
    id_type: Literal['department', 'user'],
    db_session: Session
) -> Sequence[int] | Sequence[str]:
    """
    获取部门ID列表
    Args:
        id_type (Literal['department', 'user']): 部门ID列表或用户ID列表
        db_session: 数据库会话
    Returns:
        Sequence[int] | Sequence[str]: 部门ID列表或用户ID列表
    """
    # 获取部门ID列表
    if id_type == 'department':
        department_list = db_session.scalars(
            select(QyWeixinDepartment.id)).all()
        return department_list
    # 获取用户ID列表
    elif id_type == 'user':
        user_list = db_session.scalars(
            select(QyWeixinUser.userid)).all()
        return user_list 
    else:
        raise ValueError(f"不支持的ID类型: {id_type}")

def department_user_list_to_db(
    db_session: Session,
    department_user_json: dict,
    not_user_ids: Optional[List[str] | Set[str]] = None,
) -> bool:
    """
    部门用户列表存表
    Args:
        db_session: 数据库会话
        department_user_json: 部门用户列表JSON数据
        not_user_ids: 不写入数据库的用户ID列表
    """
    user_list = department_user_json.get('userlist', [])
    # 如果用户列表为空,则返回False
    if not user_list:
        return False

    for item in user_list:
        # 如果用户ID在not_user_ids中,则跳过
        if item.get('userid') in not_user_ids:
            continue
        user = QyWeixinUser(
            userid=item.get('userid'),
            name=item.get('name'),
            position=item.get('position'),
            status=item.get('status'),
            enable=item.get('enable'),
            isleader=item.get('isleader'),
            hide_mobile=item.get('hide_mobile'),
            telephone=item.get('telephone'),
            main_department=item.get('main_department'),
            alias=item.get('alias'),
            external_position=item.get('external_position', ''),
            direct_leader=item.get('direct_leader') if item.get(
                'direct_leader') else '',
        )
        db_session.add(user)
        # 获取用户所属部门数量
        batch_number = len(item.get("department", []))
        # 遍历用户所属部门
        for i in range(batch_number):
            # 创建用户所属部门关系
            department = QyWeixinUserDepartment(
                userid=item.get('userid'),
                department_id=item.get('department')[i],
                is_leader_in_dept=item.get('is_leader_in_dept')[i],
            )
            db_session.add(department)

    return True


async def sync_department_user_list(
    forced_update: bool = False,
):
    """
    同步部门用户列表
    Args:
        forced_update (bool): 是否强制更新所有用户. Defaults to False.
    """
    # 获取数据库会话
    db = db_server(DockerPostgreSQL)
    db_session = db.get_db()

    # 获取企业微信access_token
    auth = get_access_token()
    access_token = auth.get("access_token")

    # 如果强制更新,则删除用户数据
    if forced_update:
        db.delete_data(QyWeixinUser)
        db.delete_data(QyWeixinUserDepartment)
        print("用户数据已清除!")

    # 获取部门ID列表
    department_id_list = get_id_list(
        id_type='department', db_session=db_session)
    # 获取不同步用户ID列表集合
    not_sync_user_ids = get_id_list(id_type='user', db_session=db_session)
    not_sync_user_ids = set[Any](not_sync_user_ids)

    # 遍历部门ID列表
    for department_id in department_id_list:
        # 获取部门用户列表
        department_users = await department_user_list(access_token, department_id)
        users_list = department_users.get('userlist', [])
        # 如果用户列表为空,则跳过
        if not users_list:
            print(f"部门ID为{department_id}的部门没有用户")
            continue
        # 获取用户ID列表
        users = [item.get('userid') for item in users_list]
        # 将部门用户列表存表
        response = department_user_list_to_db(
            db_session, department_users, not_user_ids=not_sync_user_ids)
        # 如果同步成功,则打印同步结果
        if response:
            print(f"部门ID为{department_id}的部门用户列表同步完成,共{len(users)}人")
        # 更新不同步用户ID列表集合
        not_sync_user_ids.update(users)
    # 提交事务
    db_session.commit()
    print("用户数据同步完成!")


if __name__ == "__main__":
    import time
    import asyncio
    start_time = time.time()

    async def main():
        await sync_department_user_list(forced_update=True)
    asyncio.run(main())
    end_time = time.time()
    print(f"执行时间: {end_time - start_time}秒")
