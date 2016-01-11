# ============== coding:utf8 ===============
from publicdefine import *


class MailDBModule(object):
    """
    struct: type(hash) mailbox   mailID   JSON(mail detail info)
    type(set) receiver mailID
    type(set) sender mailID
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
