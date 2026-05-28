"""
用户管理
    - 部门用户列表存表 department_user_list_to_db
    - 获取ID列表 get_id_list
    - 同步部门用户列表 sync_department_user_list
"""

from api.qy_weixin.http_api.access_token import get_access_token
from api.qy_weixin.http_api.user import department_user_list

from tools.async_db_connection import AsyncCallSQL
from config.server import DockerPostgreSQL

from typing import Any, List, Dict, Optional, Set
import pandas as pd

db = AsyncCallSQL(DockerPostgreSQL)


async def department_user_list_to_db(
        department_user_json: Dict,
        not_user_ids: Optional[List[str] | Set[str]] = None,
        )->bool:
    """
    部门用户列表存表
    Args:
        department_user_json (Dict): 部门用户列表JSON数据
        not_user_ids (List[str] | Set[str] | None): 不写入数据库的用户ID列表

    Returns:
        bool: 是否成功写入数据库
    """
    # 检查数据是否为空
    user_list = department_user_json.get("userlist", [])
    if not user_list:
        return False

    user_table_name = "qy_weixin_user"
    user_department_table_name = "qy_weixin_user_department"
    user_basket = []
    user_department_basket = []

    for item in user_list:
        # 检查用户是否在不写入数据库的用户ID列表中
        if item.get('userid') in not_user_ids:
            continue
        user_json = {
            'name': item.get('name'),  # 姓名 type: str
            'position': item.get('position'),  # 职位 type: str
            'status': item.get('status'),  # 人员状态 type: int
            'enable': item.get('enable'),  # 是否启用 type: int
            'isleader': item.get('isleader'),  # 是否为部门负责人 type: int
            'hide_mobile': item.get('hide_mobile'),  # 是否隐藏手机号 type: int
            'telephone': item.get('telephone'),  # 座机号 type: str
            # 主部门ID type: int
            'main_department': item.get('main_department'),
            'alias': item.get('alias'),  # 别名 type: str
            # 对外职务 type: str
            'external_position': item.get('external_position', ''),
            'userid': item.get('userid'),  # 用户ID type: str
            # 直接负责人列表 type: str
            'direct_leader': item.get('direct_leader')[0] if item.get('direct_leader', []) else '',
        }
        user_basket.append(user_json)
        # 处理人员部门信息
        batch_number = len(item.get("department", []))
        for i in range(batch_number):
            department_json = {
                'userid': item.get('userid'),  # 用户ID type: str
                'department_id': item.get('department')[i],  # 部门ID type: int
                # 是否为部门负责人 type: int
                'is_leader_in_dept': item.get('is_leader_in_dept')[i],
            }
            user_department_basket.append(department_json)
    user_df = pd.DataFrame(user_basket)
    user_department_df = pd.DataFrame(user_department_basket)
    # 写入数据库
    await db.to_sql(user_df,user_table_name,exists='append')
    await db.to_sql(user_department_df,user_department_table_name,exists='append')

    return True


async def get_id_list(
    id_type: str,):
    """
    获取ID列表
    Args:
        id_type (str): ID类型，department或user

    Returns:
        List[str]: ID列表
    """
    if id_type == 'department':
        department_sql = "select id from qy_weixin_department;"
        department_df = await db.get_data(department_sql)
        department_lsit = department_df['id'].tolist()
        return department_lsit
    elif id_type == 'user':
        user_sql = "select userid from qy_weixin_user;"
        user_df = await db.get_data(user_sql)
        user_lsit = user_df['userid'].tolist()
        return user_lsit
    else:
        raise ValueError(f"id_type must be department or user")




async def sync_department_user_list(
    forced_update: bool = False,):
    """
    同步部门用户列表
    Args:
        forced_update (bool): 是否强制更新所有用户. Defaults to False.
    """
    if forced_update:
        table_names = ['qy_weixin_user','qy_weixin_user_department']
        for table_name in table_names:
            del_sql = f"delete from {table_name};"
            await db.implement(del_sql)
            print(f"表{table_name}数据删除完成")
        
    # 获取部门ID列表
    department_id_list = await get_id_list('department')
    not_sync_user_ids = await get_id_list('user')
    not_sync_user_ids = set[Any](not_sync_user_ids)
    auth = get_access_token()
    access_token = auth.get("access_token")

    # 遍历部门ID列表，同步部门用户列表
    for department_id in department_id_list:
        department_user = await department_user_list(access_token,department_id)
        user_list = department_user.get('userlist',[])
        if not user_list:
            print(f"部门ID为{department_id}的部门没有用户")
            continue
        # 处理人员部门信息
        users = [item.get('userid') for item in user_list]
        
        response = await department_user_list_to_db(department_user,not_user_ids=not_sync_user_ids)
        not_sync_user_ids.update(users)
        if response:
            print(f"部门ID为{department_id}的部门用户列表同步完成,共{len(users)}人")



if __name__ == '__main__':
    import asyncio

    user_ids = ['ma_bo@demingjiankang.cn']
    async def main():
        await sync_department_user_list(forced_update=True)

    asyncio.run(main())
    