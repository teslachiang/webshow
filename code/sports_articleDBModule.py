# ============== coding:utf8 ===============
from publicdefine import *


class ArticleDBModule(object):
    """
    """

    def __init__(self, ):
        """
        """
        redispool = redis.ConnectionPool(host='localhost',
                                           port=6380,
                                           db=0,
                                           password='jianglei0711')
        redis_server = redis.Redis(connection_pool=redispool)
        self.redis_server = redis_server
        self.redis_pipe = self.redis_server.pipeline()

    def sportstypes(self, menujson):
        return self.redis_server.set("sports:types", ujson.dumps(menujson))

    def getsportstypes(self):
        """
        """
        menujson = self.redis_server.get("sports:types")
        if menujson is None:
            return -1
        try:
            return ujson.loads(menujson)
        except:
            return -2


def main():
    adb = ArticleDBModule()
    menujson = ujson.load(open("menu.json"))
    adb.sportstypes(menujson)


if __name__ == '__main__':
    main()
