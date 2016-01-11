# =========coding:utf8=========
import redis
import ujson
from publicdefine import *


def redisreadtest(redis_server):
    username = "25422875@qq.com"
    umd5 = md5value(username)
    _tmp = redis_server.hget("sports:users", umd5)
    if _tmp is None:
        return -2
    #uobj = ujson.loads(_tmp)
    #return uobj

from datetime import datetime


def main():
    """
    """

    redispool = redis.ConnectionPool(host='localhost',
                                           port=6380,
                                           db=0,
                                           password='jianglei0711')
    redis_server = redis.Redis(connection_pool=redispool)
    start = datetime.now()
    for i in range(10000000):
        redisreadtest(redis_server)
    end = datetime.now()
    print 'total cost: ', (end-start).seconds

if __name__ == '__main__':
    main()
