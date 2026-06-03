"""
部门管理
    - 部门数据插入 insert_department_data
    - 获取部门列表 get_department_list
    - 部门列表插入数据库 department_list_to_db
"""

from utils.db_link import db_server

from configs.server import DockerPostgreSQL

from api.qy_weixin.data_manipulation.models import QyWeixinDepartment
from api.qy_weixin.http_api.department import department_list
from api.qy_weixin.http_api.access_token import get_access_token

from sqlalchemy.orm.session import Session


def insert_department_data(db_session: Session, department_json: dict) -> QyWeixinDepartment:
    """
    部门数据插入
    Args:
        db_session: 数据库会话
        department_json: 部门数据
    Returns:
        department_new: 部门数据
    """
    department_new = QyWeixinDepartment(
        id=department_json.get('id'),
        name=department_json.get('name'),
        parentid=department_json.get('parentid'),
        order=department_json.get('order'),
        department_leader=department_json.get('department_leader')[
            0] if department_json.get('department_leader') else '',
    )
    db_session.add(department_new)
    # db_session.commit()
    return department_new


async def get_department_list():
    """
    获取部门列表
    Returns:
        departments: 部门列表
    """
    data = get_access_token()
    access_token = data.get('access_token')
    data = await department_list(access_token)
    if data.get('errcode', -1) == 0:
        departments = data.get('department', [])
        if not departments:
            return False
        return departments
    else:
        print(f"获取部门列表失败,错误码: {data.get('errcode')},错误信息: {data.get('errmsg')}")
        return None


def department_list_to_db(departments: list, forced_update: bool = False):
    """
    部门列表插入数据库
    Args:
        departments: 部门列表
        forced_update: 是否强制更新
    """
    if not departments:
        print("部门列表为空")
        return
    data_base = db_server(DockerPostgreSQL)

    if forced_update:
        data_base.delete_data(QyWeixinDepartment)
        print("部门数据表数据删除完成")

    # 获取数据库会话
    db_session = data_base.get_db()

    success = 0
    failure = 0

    for department in departments:
        department_new = insert_department_data(db_session, department)
        if department_new:
            success += 1
        else:
            failure += 1
    db_session.commit()
    print(f"成功插入{success}条数据，失败{failure}条数据")


if __name__ == "__main__":
    import asyncio
    import time


    start_time = time.time()
    departments = asyncio.run(get_department_list())
    department_list_to_db(departments, forced_update=False)
    end_time = time.time()
    print(f"执行时间: {end_time - start_time}秒")