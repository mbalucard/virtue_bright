"""
日历管理
    - 获取日历详情 get_calendar_info
    - 删除日历 delete_calendar
    - 创建日历 create_calendar
    - 更新日历 update_calendar
"""

from api.qy_weixin.http_api.oa import get_calendar, del_calendar, add_calendar, update_calendar
from api.qy_weixin.http_api.access_token import get_access_token

from tools.async_db_connection import AsyncCallSQL
from config.server import DockerPostgreSQL

import pandas as pd
from typing import Optional

db = AsyncCallSQL(DockerPostgreSQL)


async def get_calendar_info(
        cal_id: str,
        update_db: bool = False) -> Optional[pd.DataFrame]:
    """
    获取日历详情
    Args:
        cal_id (str): 日历ID
        update_db (bool, optional): 是否更新数据库. Defaults to False.
            - True: 从企业微信获取数据并更新数据库
            - False: 从数据库获取数据,如果不存在,则从企业微信获取数据并插入数据库
    Returns:
        Optional[pd.DataFrame]: 日历详情, 如果不存在则返回None
    """
    if not update_db:
        # 从数据库获取数据
        select_sql = f"""
        SELECT * FROM qy_weixin_calendar WHERE cal_id = '{cal_id}';
        """
        df = await db.get_data(select_sql)
        if not df.empty:
            # print("已在数据库中找到数据")
            return df

    # 获取access_token
    auth = get_access_token()
    access_token = auth["access_token"]
    # 从企业微信获取数据
    #! 该接口支持批量更新或插入数据，出于谨慎，该函数入参并未这么操作
    data_json = await get_calendar(access_token, cal_id_list=[cal_id])
    if data_json.get("errcode", -1) == 0:
        # print("企业微信返回数据成功,开始处理数据")
        calendar_list = data_json.get("calendar_list", [])
        if calendar_list:
            basket = []  # 一揽子工程
            for item in calendar_list:
                # 构建数据
                calendar_json = {
                    "cal_id": item["cal_id"],  # 日历ID 主键
                    "summary": item["summary"],  # 日历标题
                    "description": item["description"],  # 日历描述
                    "is_public": item["is_public"],  # 是否公共日历
                    "is_corp_calendar": item["is_corp_calendar"],  # 是否企业日历
                    "admin": item["admins"][0],  # 日历管理员用户ID
                }
                basket.append(calendar_json)  # 为插入数据行准备

                # 更新数据表
                if update_db:
                    await db.update(
                        table_name="qy_weixin_calendar",
                        values=calendar_json,
                        where_condition="cal_id = :cal_id",
                        params={"cal_id": cal_id},
                    )

            # 插入数据表
            if not update_db:
                df = pd.DataFrame(basket)
                await db.to_sql(
                    data_frame=df,
                    table_name="qy_weixin_calendar", exists="append")
                # print("数据已成功写入数据库,重新从数据库获取数据")
            # 重新获取数据
            df = await get_calendar_info(cal_id, update_db=False)
            return df
        else:
            # print("企业微信返回数据成功,但日历列表为空")
            return None
    else:
        print(f"企业微信返回数据失败:{data_json}")
        return None


async def delete_calendar(cal_id: str) -> bool:
    """
    删除日历
    Args:
        cal_id (str): 日历ID
    Returns:
        bool: 是否删除成功
    """
    df = await get_calendar_info(cal_id)
    if not df.empty:
        await db.update(
            table_name="qy_weixin_calendar",
            values={"is_delete": 1},
            where_condition="cal_id = :cal_id",
            params={"cal_id": cal_id},
        )
        print(f"已将日历{cal_id}标记为删除")
        auth = get_access_token()
        access_token = auth["access_token"]
        data_json = await del_calendar(access_token, cal_id)
        if data_json.get("errcode", -1) == 0:
            return True
        else:
            print(f"企业微信删除日历失败:{data_json}")
            return False
    else:
        return False


async def create_calendar(
        summary: str,
        color: str = "#FF3030",
        description: Optional[str] = None,
        admins: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        permission: int = 1,
        is_public: int = 0,
        partyids: Optional[List[int]] = None,
        set_as_default: int = 0,
        is_corp_calendar: int = 0,) -> Optional[pd.DataFrame]:
    """
    创建日历
    Args:
        summary(str): 日历标题
        color(str): 日历颜色 Default: "#FF3030"
            - 颜色值为RGB颜色编码16进制表示
        description(str,None): 日历描述 Default: None
            - 长度不能超过255个字符
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
        Optional[pd.DataFrame]: 日历信息或None
    """
    sql = f"""
    select summary from qy_weixin_calendar where summary = '{summary}' and is_delete = 0;
    """
    df = await db.get_data(sql)
    if not df.empty:
        print(f"创建失败：日历{summary}已存在")
        return None

    auth = get_access_token()
    access_token = auth["access_token"]
    data_json = await add_calendar(
        access_token,
        summary=summary,
        color=color,
        description=description,
        admins=admins,
        userids=userids,
        permission=permission,
        is_public=is_public,
        partyids=partyids,
        set_as_default=set_as_default,
        is_corp_calendar=is_corp_calendar,
    )
    if data_json.get("errcode", -1) == 0:
        cal_id = data_json.get("cal_id")
        df = await get_calendar_info(cal_id)
        return df
    else:
        print(f"企业微信创建日历失败:{data_json}")
        return None


async def update_calendar_info(
        cal_id: str,
        summary: str,
        color: str = "#FF3030",
        description: Optional[str] = None,
        skip_public_range: int = 0,
        admins: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        permission: int = 1,
        partyids: Optional[List[int]] = None,) -> Optional[pd.DataFrame]:
    """
    更新日历信息
    Args:
        cal_id (str): 日历ID
        summary(str): 日历标题
        color(str): 日历颜色 Default: "#FF3030"
            - RGB颜色编码16进制表示
        description(str,None): 日历描述 Default: None
        skip_public_range(int): 是否不更新可订阅范围 Default: 0 会更新可订阅范围
            - 0-否 1-是
        admins(list[str],None): 日历管理员用户ID列表, Default: None 不更新
            - 最多指定3人
            - 空 list 表示清空管理员
        userids(list[str],None): 日历通知范围成员用户ID列表, Default: None
            - 最多指定1000人
            - 空 list 表示清空人员
        permission(int): 日历通知范围成员权限 Default: 1
            - 1-查看 3-仅查看闲忙状态
        partyids(list[int],None): 公开给指定部门ID列表, Default: None
            - 最多指定100个部门
            - 空 list 表示清空部门
    Returns:
        Optional[pd.DataFrame]: 日历信息或None
    """
    df = await get_calendar_info(cal_id)
    if df.empty:
        print(f"更新失败：日历{cal_id}不存在")
        return None

    auth = get_access_token()
    access_token = auth["access_token"]
    calendar_data = await get_calendar(
        access_token,
        cal_id_list=[cal_id],
    )

    if calendar_data.get("errcode", -1) != 0:
        print(f"企业微信获取日历失败:{calendar_data}")
        return None

    if admins is None:
        calendar_list = calendar_data.get("calendar_list")
        print(calendar_list)
        admins = calendar_list[0].get("admins")

    if calendar_data.get("is_public", 0) == 1:
        public_range = calendar_data.get("public_range")
        if userids is None:
            userids = public_range.get("userids")
        if partyids is None:
            partyids = public_range.get("partyids")

    data_json = await update_calendar(
        access_token,
        cal_id=cal_id,
        summary=summary,
        color=color,
        description=description,
        skip_public_range=skip_public_range,
        admins=admins,
        userids=userids,
        permission=permission,
        partyids=partyids,
    )
    if data_json.get("errcode", -1) == 0:
        df = await get_calendar_info(cal_id, update_db=True)
        return df
    else:
        print(f"企业微信更新日历失败:{data_json}")
        return None


if __name__ == '__main__':
    import asyncio

    cal_id = "wcsBwaDgAAxcEvjTn9XkJ9C4T5BOoo4Q"
    user_id = "ma_bo@demingjiankang.cn"

    async def main():
        data = await update_calendar_info(
            cal_id=cal_id,
            summary="test日历",
            # admins=[user_id],
            description="用来个人测试",
        )
        print(data)

    asyncio.run(main())
    # data = asyncio.run(delete_calendar(cal_id))
    # print(data)
