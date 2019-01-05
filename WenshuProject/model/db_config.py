# coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import platform

pl = platform.system()
if pl == "Linux":
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/tax?charset=utf8mb4')
else:
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/tax?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)


class RedisPool:
    if pl == "Windows":
        def __init__(self, client_host="127.0.0.1", client_port=6379, client_db=0):
            self.client_host = client_host
            self.client_port = client_port
            self.client_db = client_db
    else:
        def __init__(self, client_host="127.0.0.1", client_port=6379, client_db=0):
            self.client_host = client_host
            self.client_port = client_port
            self.client_db = client_db

    def redis_pool(self):
        if pl == "Windows":
            pool = redis.ConnectionPool(
                host=self.client_host,
                port=self.client_port,
                db=self.client_db)
        else:
            pool = redis.ConnectionPool(
                host=self.client_host,
                port=self.client_port,
                db=self.client_db)
        return redis.StrictRedis(connection_pool=pool)


if __name__ == '__main__':
    r = RedisPool(client_db=1)
    rp = r.redis_pool()
    page = rp.get("hei_page")
    if not page:
        rp.set("hei_page", 1)
    rp.incrby("hei_page", 1)
    print(int(page.decode()))
