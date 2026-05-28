"""
部门管理
    - 同步部门到数据库 sync_department
"""

from api.qy_weixin.http_api.access_token import get_access_token
from api.qy_weixin.http_api.department import department_list

from tools.async_db_connection import AsyncCallSQL
from config.server import DockerPostgreSQL

import pandas as pd

db = AsyncCallSQL(DockerPostgreSQL)


async def sync_department(
    forced_update: bool = False) -> bool:
    """
    同步部门到数据库
    Args:
        forced_update (bool, optional): 是否强制更新. Defaults to False.
    Returns:
        bool: 是否同步成功
    """
    table_name = "qy_weixin_department"
    sql_check = f"select count(id) from {table_name};"
    sql_val = await db.get_data(sql_check)
    if sql_val['count'].item() == 0:
        print("数据库数据为空，开始同步部门列表")
        response = get_access_token()
        access_token = response['access_token']
        data = await department_list(access_token)
        if data.get('errcode', -1) == 0:
            print("获取部门列表成功")
            departments = data.get('department', [])
            if not departments:
                print("部门列表为空")
                return False
            # 处理部门负责人
            basket = []
            for item in departments:
                # 处理部门负责人为list的情况
                if isinstance(item.get('department_leader', []), list):
                    # 如果有值，取第一个
                    if item.get('department_leader'):
                        item['department_leader'] = item.get(
                            'department_leader')[0]
                    # 没有值的情况，设为空字符串
                    else:
                        item['department_leader'] = ''
                    basket.append(item)
                else:
                    basket.append(item)
            # 存储至数据库
            df = pd.DataFrame(basket)
            await db.to_sql(
                df,
                table_name=table_name,
                exists="append"
            )
            print("部门列表同步到数据库成功")
            return True

        else:
            print(f"获取部门列表失败:{data}")
            return False

    else:
        if forced_update:
            sql_delete = f"delete from {table_name};"
            await db.implement(sql_delete)
            print("数据表已清空")
            result = await sync_department(forced_update=False)
            return result
        else:
            print(f"数据表已有值:{sql_val['count'].item()} 行。")
            return False


if __name__ == "__main__":
    import asyncio
    test_result = asyncio.run(sync_department(forced_update=True))
    print(test_result)
