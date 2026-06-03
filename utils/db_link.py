from sqlalchemy import create_engine,delete
from sqlalchemy.orm import sessionmaker


class db_server:
    """
    数据库连接
    支持 MySQL (pymysql) 和 PostgreSQL (psycopg2) 和 MSSQL (pymssql)
    """
    def __init__(self, server: object):
        """
        :param server: 服务器连接方式,类型class, 必须包含type、user、password、ip、database属性
        """
        self.server = server

        if self.server.type == 'sqlserver':
            self.method = 'mssql+pymssql'
        elif self.server.type == 'MySQL':
            self.method = 'mysql+pymysql'
        elif self.server.type == 'PostgreSQL':
            self.method = 'postgresql+psycopg2'
        else:
            raise ValueError(
                f"不支持的数据库类型: {self.server.type}。目前仅支持 'MySQL', 'PostgreSQL' 和 'MSSQL'.")

        self.conn_parameter = f"{self.method}://{self.server.user}:{self.server.password}@{self.server.host}/{self.server.database}"
        if self.server.type == 'MSSQL':
            self.conn_parameter += "?charset=utf8"
        self.engine = create_engine(self.conn_parameter, echo=False)

    def _get_session(self):
        """创建会话工厂"""
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        return SessionLocal

    def _db_generator(self):
        """获取数据库会话"""
        SessionLocal = self._get_session()
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_db(self):
        return next(self._db_generator())

    def get_engine(self):
        """获取数据库引擎"""
        return self.engine

    def delete_data(self, table_name: str):
        """删除数据表"""
        db = self.get_db()
        try:
            db.execute(delete(table_name))
            db.commit()
            return True
        finally:
            db.close()


if __name__ == "__main__":
    from configs.server import DockerPostgreSQL
    db = db_server(DockerPostgreSQL)
    print(db.get_db())