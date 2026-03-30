import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import ProgrammingError, OperationalError
from typing import Union, AsyncGenerator, Optional

pd.set_option('display.unicode.east_asian_width', True)


class AsyncCallSQL:
    """
    调用数据库 (异步版本)
    支持 MySQL (aiomysql) 和 PostgreSQL (asyncpg)
    """

    def __init__(self, server: object):
        """
        Args:
            server (object): 服务器连接对象，需包含 type, user, password, host, database 属性
        """
        self.sql = server
        self.server_type = getattr(self.sql, 'type', None)

        if self.server_type == 'MySQL':
            driver = 'mysql+aiomysql'
            use_charset = True
        elif self.server_type == 'PostgreSQL':
            driver = 'postgresql+asyncpg'
            use_charset = False
        else:
            raise ValueError(
                f"不支持的数据库类型: {self.server_type}。目前仅支持 'MySQL' 和 'PostgreSQL'")

        # 构建基础连接字符串
        base_url = f"{driver}://{self.sql.user}:{self.sql.password}@{self.sql.host}/{self.sql.database}"

        # 构建查询参数
        params = []
        if use_charset:
            params.append("charset=utf8")

        if params:
            self.conn_parameter = f"{base_url}?{'&'.join(params)}"
        else:
            self.conn_parameter = base_url

        self.engine = create_async_engine(self.conn_parameter, echo=False)

    async def get_data(self, sql_command: str, chunksize: Optional[int] = None) -> Union[pd.DataFrame, AsyncGenerator[pd.DataFrame, None]]:
        """
        根据语句获取数据 (异步)
        Args:
            sql_command(str): 数据库执行命令
            chunksize(int, None): 每次读取的行数 Defaults: None.
                - None 表示一次读取所有行
        Returns:
            DataFrame: 查询结果
        """
        if chunksize is None:
            async with self.engine.connect() as conn:
                # 执行异步查询
                result = await conn.execute(text(sql_command))
                # 将结果转换为 DataFrame
                data = pd.DataFrame(result.fetchall(),
                                    columns=list(result.keys()))
            return data
        else:
            async def _chunk_generator() -> AsyncGenerator[pd.DataFrame, None]:
                async with self.engine.connect() as conn:

                    result = await conn.stream(text(sql_command))
                    keys = list(result.keys())

                    while True:
                        rows = await result.fetchmany(chunksize)
                        if not rows:
                            break
                        yield pd.DataFrame(rows, columns=keys)

            return _chunk_generator()

    async def implement(self, sql_command: str) -> None:
        """
        根据语句对数据库进行操作 (异步)
        Args:
            sql_command(str): 数据库执行命令
        """
        async with self.engine.begin() as conn:
            await conn.execute(text(sql_command))
        print('Mission accomplished!')

    async def to_sql(self, data_frame: pd.DataFrame, table_name: str, exists: str = 'fail', size: int = None) -> None:
        """
        将DataFrame插入至数据库 (异步)
        注意: pandas 的 to_sql 本身是同步的，这里使用 run_sync 在异步引擎中运行它。
        Args:
            data_frame (pd.DataFrame): 要插入的DataFrame。
            table_name (str): 数据库中的目标表名。
            exists (str, optional): 如果表已存在，'fail' 会引发错误，'replace' 会替换表，'append' 会追加数据。默认值为 'fail'。
            size (int, optional): 每次批量插入的行数。如果为 None，则一次插入所有行。默认值为 None。
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(
                lambda c: data_frame.to_sql(
                    table_name,
                    c,
                    index=False,
                    if_exists=exists,
                    chunksize=size
                )
            )
        print(f'数据已写入 {table_name} 中')

    async def update(self, table_name: str, values: dict, where_condition: str, params: dict = None):
        """
        更新数据库中的数据 (异步)。
        Args:
            table_name (str): 需要更新的表名。
            values (dict): 一个字典，包含要更新的列和对应的新值。
            where_condition (str): 更新条件的SQL字符串, e.g., "id = :id AND name = :name"。
                - 请使用命名参数（如 :id）来避免SQL注入。
            params (dict, optional): 一个字典，为WHERE条件中的命名参数提供值, e.g., {"id": 1, "name": "NewName"}。
        """
        if not values:
            print("没有提供要更新的数据。")
            return

        set_clause = ", ".join([f"{key} = :{key}" for key in values.keys()])
        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_condition}"

        all_params = values.copy()
        if params:
            all_params.update(params)

        try:
            async with self.engine.begin() as conn:
                await conn.execute(text(sql_query), all_params)
            # print(f"表 {table_name} 的数据已成功更新。")
        except Exception as e:
            print(f"更新数据时出错: {e}")
            raise

    async def table_exists(self, table_name: str) -> bool:
        """
        判断指定表是否存在 (通过尝试查询并捕获异常)
        Args:
            table_name (str): 需要检查的表名
        Returns:
            bool: True 表示存在, False 表示不存在
        """
        # 这里假设 table_name 是内部构造的、可信的表名
        sql = text(f"SELECT 1 FROM {table_name} LIMIT 1")

        async with self.engine.connect() as conn:
            try:
                await conn.execute(sql)
                return True
            except (ProgrammingError, OperationalError) as e:
                # 不同数据库/驱动的错误信息略有不同，这里用字符串判断一下
                msg = str(e).lower()
                # 常见：mysql -> "doesn't exist"; postgresql -> "does not exist" / "undefined table"
                if "doesn't exist" in msg or "does not exist" in msg or "undefined table" in msg:
                    return False
                # 其它类型的错误（比如权限问题等）直接抛出去
                raise

    async def close(self):
        """关闭数据库连接池"""
        await self.engine.dispose()


if __name__ == '__main__':
    import asyncio
    from configs.server import DockerPostgreSQL

    # 测试 PostgreSQL
    async def test_async_pg():
        print("--- Testing PostgreSQL ---")
        sql_command = r"select * from qy_weixin_user limit 5;"
        data_async = AsyncCallSQL(DockerPostgreSQL)
        try:
            df = await data_async.get_data(sql_command)
            print("异步 PostgreSQL 获取数据成功:")
            print(df)
        finally:
            await data_async.close()


    async def main():
        await test_async_pg()
        # await test_async_mysql() # 如果需要测试 MySQL，取消注释

    asyncio.run(main())
