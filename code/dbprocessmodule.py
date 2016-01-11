# ============== coding:utf8 ===============
from publicdefine import *


class DBProcessModule(object):
    """
    """

    def __init__(self, ):
        """
        """
        redispool = redis.ConnectionPool(host='localhost',
                                           port=6379,
                                           db=0,
                                           password='jianglei0711')
        redis_server = redis.Redis(connection_pool=redispool)
        self.redis_server = redis_server
        self.redis_pipe = self.redis_server.pipeline()

    def setadmininfo(self, email, password):
        """
        """
        obj = {'password': password, 'articles': []}
        self.redis_pipe.hset("sports:admins", email, ujson.dumps(obj))
        self.redis_pipe.execute()
    # ====    2015年 12月 10日 星期四

    def searcharticleswithkeywords(self, keyword):
        pass

    def getuserspecial(self, userid):
        special = None
        # query user special and return it
        return special

    def getarticlebyid(self, artid):
        """
        """
        artstr = self.redis_server.hget("sports:admin:articles", artid)
        if artstr is None:
            return -1
        try:
            return ujson.loads(artstr)
        except Exception as e:
            return -2

    def gethotarticles(self, special=None):
        akeys = self.redis_server.hkeys("sports:admin:articles")

        def __summaryinfo__(srcjson):
            srcobj = ujson.loads(srcjson)
            if special is not None:
                # here need to add a filter by user special info
                pass
            return {'tags': srcobj['tags'],
                    'artid': srcobj['articleid'],
                    'block': srcobj['block'],
                    'title': srcobj['title'],
                    'timestamp': srcobj['timestamp']}
        arts = [__summaryinfo__(self.redis_server.hget("sports:admin:articles", k)) for k in akeys]
        return sorted(arts, key=lambda k: parse(k['timestamp']), reverse=True)

    # ==== END === 2015年 12月 10日 星期四

    def updateblocks(self, mlist):
        """
        """
        if mlist is None or len(mlist) == 0:
            return
        self.redis_server.delete("sports:blocks")
        [self.redis_pipe.sadd("sports:blocks", m) for m in mlist if m is not None]
        self.redis_pipe.execute()

    def queryblocks(self, keyword):
        if keyword is None or len(keyword.strip()) == 0:
            return
        blocks = self.redis_server.smembers("sports:blocks")
        if keyword == u"*":
            return blocks
        return [b for b in blocks if b.find(keyword) >= 0]

    def _dbaddarticle2block(self):
        """
        """
        #blocks = self.redis_server.smembers("sports:blocks")
        artvals = self.redis_server.hvals("sports:admin:articles")
        for art in artvals:
            artobj = ujson.loads(art)
            aid = artobj['articleid']
            self.redis_pipe.sadd("sports:block:%s"%md5value(artobj['block']), aid)
            #self.redis_pipe.hdel("sports:admin:articles", aid)
            self.redis_pipe.execute()

    def dbqueryblockarticles(self, email, block, keyword):
        """
        """
        if block is None or email is None:
            return -1
        artids = self.redis_server.smembers("sports:block:%s"%md5value(block))
        if artids is None or len(artids) == 0:
            return []
        articles = self.dbadmingetarticles(email)
        if type(articles) == int:
            return -2
        # print keyword, artids, block
        # _tmp = []
        # _tmp.extend(artids)
        # print "-------->", _tmp
        # for a in articles:
        #     if '%s'%a['id'] in artids:
        #         print a['title'], a['id']
        #         print a['title'].find(keyword)
        if keyword == "*" or keyword is None:
            return [a for a in articles if '%s'%a['id'] in artids]
        else:
            return [a for a in articles if '%s'%a['id'] in artids and a['title'].find(keyword)>=0]

    def createarticleid(self):
        return self.redis_server.incr("sports:admin:articleid")

    def dbadmingetarticles(self, email):
        """
        """
        adinfo = self.redis_server.hget("sports:admins", email)
        if adinfo is None:
            return -1
        try:
            adinfoobj = ujson.loads(adinfo)
            articles = adinfoobj.get('articles')
            return articles
        except Exception as e:
            print traceback.print_exc()
            return -2

    def dbgetadminarticle(self, artid):
        if artid is None:
            return -1
        artstr = self.redis_server.hget("sports:admin:articles", artid)
        if artstr is None:
            return -2
        try:
            artobj = ujson.loads(artstr)
            if artobj is None:
                return -3
            return artobj
        except Exception as e:
            print e
            return -3

    def dbadminremovearticle(self, email, artid):
        """
        """
        if artid is None or email is None:
            return -1
        adinfo = self.redis_server.hget("sports:admins", email)
        if adinfo is None:
            return -2
        try:
            adinfoobj = ujson.loads(adinfo)
            articles = adinfoobj.get('articles')
            if articles is None:
                return -3

            [articles.remove(a) for a in articles if a['id'] == int(artid)]

            adinfoobj['articles'] = articles
            print adinfoobj['articles']
            # set info to admin
            self.redis_pipe.hset("sports:admins", email, ujson.dumps(adinfoobj))
            artstr = self.redis_server.hget("sports:admin:articles", artid)
            artobj = ujson.loads(artstr)
            self.redis_pipe.srem("sports:block:%s"%md5value(artobj['block']), artid)
            self.redis_pipe.hdel("sports:admin:articles", artid)
            self.redis_pipe.execute()
            return 0
        except Exception as e:
            print e
            return -4

    def dbadminmodifyarticle(self, email, artid, artobj):
        """
           the user only allow to modify self articles
        """
        if artid is None or email is None:
            return -1
        adinfo = self.redis_server.hget("sports:admins", email)
        if adinfo is None:
            return -2
        try:
            artid = int(artid)
            adinfoobj = ujson.loads(adinfo)
            articles = adinfoobj.get('articles')
            if artid not in [int(a['id']) for a in articles if type(a) == dict]:
                # article not in user's article list
                print "article not in list"
                return -3
            elem = {'id': int(artobj['articleid']), 'title': artobj['title'],
                    'createtime': artobj['timestamp'],
                    'modifytime': artobj.get('modify_timestamp')}
            _s = stringfiltersymbol(elem['title'])
            if _s is None:
                return -4
            _atmd5s = []

            for a in articles:
                if type(a) == dict:
                    if int(a['id']) != artid:
                        _atmd5s.append(a['t_md5'])
                    else:
                        print "=======remove old art=======", a
                        articles.remove(a)
            _tmd5 = md5value(_s.decode('utf8'))
            if _tmd5 not in _atmd5s:
                elem['t_md5'] = _tmd5
                adinfoobj['articles'].insert(0, elem)
                self.redis_pipe.hset("sports:admins", email, ujson.dumps(adinfoobj))
                #
                oldart = self.redis_server.hget("sports:admin:articles", artid)
                oldartobj = ujson.loads(oldart)
                if oldartobj['block'] != artobj['block']:
                    self.redis_pipe.srem("sports:block:%s"%md5value(oldartobj['block']), artid)
                    self.redis_pipe.sadd("sports:block:%s"%md5value(artobj['block'].decode('utf8')), artid)
                self.redis_pipe.hset("sports:admin:articles", artid, ujson.dumps(artobj))
                self.redis_pipe.execute()
                return 0
            else:
                return -5  # same title in list
        except Exception as e:
            print traceback.print_exc()
            return -6

    def dbadminaddarticle(self, email, artobj):
        """
        """
        adinfo = self.redis_server.hget("sports:admins", email)
        if adinfo is None:
            return -1
        try:
            adinfoobj = ujson.loads(adinfo)
            articles = adinfoobj.get('articles')
            elem = {'id': int(artobj['articleid']), 'title': artobj['title'],
                    'createtime': artobj['timestamp'],
                    'modifytime': artobj.get('modify_timestamp')}

            if articles is None:
                adinfoobj['articles'] = [elem]
            else:
                _s = stringfiltersymbol(elem['title'])
                if _s is None:
                    return -4
                _atmd5s = [a['t_md5'] for a in articles if type(a) == dict]
                _tmd5 = md5value(_s.decode('utf8'))
                if _tmd5 not in _atmd5s:
                    elem['t_md5'] = _tmd5
                    adinfoobj['articles'].insert(0, elem)
                else:
                    return -3

            # set info to admin
            self.redis_pipe.hset("sports:admins", email, ujson.dumps(adinfoobj))
            # add article to db
            self.redis_pipe.sadd("sports:block:%s"%md5value(artobj['block'].decode('utf8')), artobj['articleid'])
            self.redis_pipe.hset("sports:admin:articles", artobj['articleid'], ujson.dumps(artobj))
            self.redis_pipe.execute()
            return 0
        except Exception as e:
            print e
            print traceback.print_exc()
            return -2

    def dbcheckuser(self, email, password, pwmd5=False):
        """
        """
        if email is None or password is None:
            return -1
        email = email.strip()
        adinfo = self.redis_server.hget("sports:admins", email)
        if adinfo is None:
            return -2
        try:
            adinfoobj = ujson.loads(adinfo)
        except:
            return -3
        if pwmd5:
            _md5value = md5value
            if _md5value(adinfoobj.get('password')) == password:
                return {'articles': adinfoobj.get('articles')}
            else:
                return -4
        if adinfoobj.get('password') == password:
            return {'articles': adinfoobj.get('articles')}
        else:
            return -4


def main():
    """
    """
    # menu = ujson.load(open("menu.json"))
    # ret = []
    # [ret.extend(menu.get(k)) for k in menu.keys()]
    # for r in ret:
    #     print r
    db = DBProcessModule()
    db._dbaddarticle2block()
    return
    email = "25422875@qq.com"
    password = "jianglei0711"
    db = DBProcessModule()
    db.setadmininfo(email, password)

    print "done!"


if __name__ == '__main__':
    main()
