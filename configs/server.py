import os
from dotenv import load_dotenv


load_dotenv()


class DockerPostgreSQL:
    """docker-postgresql"""
    type = 'PostgreSQL'
    user = os.getenv('DockerPostgreSQLUser')
    password = os.getenv('DockerPostgreSQLPassword')
    host = os.getenv('DockerPostgreSQLHost')
    database = os.getenv('DockerPostgreSQLDatabase')


class RedisServer:
    Host = os.getenv('RedisHost')
    Port = os.getenv('RedisPort')
    Password = os.getenv('RedisPassword')
    DB = os.getenv('RedisDB')
    TTL = os.getenv('RedisTTL')


if __name__ == '__main__':
    print(DockerPostgreSQL.host)
    print(RedisServer.Host)
    print(DockerPostgreSQL.database)