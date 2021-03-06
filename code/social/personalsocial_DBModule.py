# ============== coding:utf8 ===============
import sys
import os
sys.path.append(os.path.abspath(os.path.pardir))
from publicdefine import *


class SocialDBProcessModule(object):
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

        redispool_admindb = redis.ConnectionPool(host='localhost',
                                                 port=6379,
                                                 db=0,
                                                 password='jianglei0711')
        self.redis_server_admindb = redis.Redis(connection_pool=redispool_admindb)
        self.redis_pipe = self.redis_server.pipeline()

    def __userquerykey__(self):
        for uk in self.redis_server.hkeys("sports:users"):
            userjson = self.redis_server.hget("sports:users", uk)
            ujsonobj = ujson.loads(userjson)
            print uk, ujsonobj['username']
            self.redis_server.set("sports:%s:user"%uk, "%s:%s"%(ujsonobj['username'], ujsonobj['nickname']))
    
    def queryuserwithkeywords(self, keywords):
        """
        query user with keyword, nickname or mailinfo
        """
        kyws = re.split(";|:|,|\s|?", keywords.strip())
        ret = []
        for su in self.redis_server.keys("sports:*:user"):
            su_val = self.redis_server.get(su)
            for k in kyws:
                if len(k) > 0 and su_val.find(k) >= 0:
                    ret.append(su.split(":")[1])
                    break
        return ret
    
    def updatearticleinfo(self, username, articleid, contentobj):
        """
        """
        md5name = md5value(username.strip())
        articledbid = "%s_%s"%(md5name,articleid.strip())
        userarticle = self.redis_server.hget("sports:circle:articles", articledbid)
        try:
            if userarticle is None:
                dbelem = {'content': None, 'images': []}
                _c = contentobj.get('content')
                if _c is not None:
                    dbelem['content'] = _c
                _i = contentobj.get('image')
                if _i is not None:
                    dbelem['images'].append(_i)
                self.redis_pipe.hset("sports:circle:articles", articledbid, ujson.dumps(dbelem))
            else:
                artobj = ujson.loads(userarticle)
                _c = contentobj.get('content')
                if _c is not None:
                    artobj['content'] = _c
                _i = contentobj.get('image')
                if _i is not None and _i not in artobj['images']:
                    artobj['images'].append(_i)
                self.redis_pipe.hset("sports:circle:articles", articledbid, ujson.dumps(artobj))
            self.redis_pipe.execute()
            return 0
        except Exception as e:
            print traceback.print_exc()
            return -1

    def createnewcircle(self, username, circleobj):
        """
        """
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        circles = userobj[1].get('circles')
        md5name = md5value(circleobj['circlename'])
        if circles is None:
            userobj[1].set('circles', {md5name: circleobj})
        else:
            if md5name not in circles.keys():
                userobj[1]['circles'][md5name] = circleobj
                self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
                self.redis_pipe.execute()
            else:
                return -11
        return 0

    def updateusercircle(self, username, circlemd5name, circleobj):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        circles = userobj[1].get('circles')
        if circles is None:
            return -11
        circleold = circles.get(circlemd5name)
        if circleold is None:
            return -12
        if userobj[1]['circles'].pop(circlemd5name) is None:
            return -13
        md5name = md5value(circleobj['circlename'])
        if md5name not in circles.keys():
            userobj[1]['circles'][md5name] = circleobj
            self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
            self.redis_pipe.execute()
        else:
            return -14
        return 0

    def getusercircles(self, username):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        circles = userobj[1].get('circles')
        if circles is None:
            return {}
        else:
            return circles

    def cleansubject(self, username, subject):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        subjects = userobj[1].get('subjects')
        if subjects is None:
            return -12
        else:
            print subjects
            assignedsub = subjects.get(subject)
            if assignedsub is None:
                return -11
            userobj[1]['subjects'].pop(subject)
            print userobj[1]['subjects']
            self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
            self.redis_pipe.execute()
        return 0

    def userremovesuject(self, username, subject):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        subjects = userobj[1].get('subjects')
        if subjects is None:
            return -12
        else:
            assignedsub = subjects.get(subject)
            if assignedsub is None:
                return -11
        userobj[1]['subjects'][subject]['isremoved'] = True

        self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
        self.redis_pipe.execute()
        return 0

    def usertogglesuject(self, username, subject, isclose=False):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        subjects = userobj[1].get('subjects')
        if subjects is None:
            return -12
        else:
            assignedsub = subjects.get(subject)
            if assignedsub is None:
                return -11
        __isclosed = assignedsub.get('isclosed')
        if __isclosed is None:
            userobj[1]['subjects'][subject]['isclosed'] = False
        else:
            userobj[1]['subjects'][subject]['isclosed'] = isclose

        self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
        self.redis_pipe.execute()
        return 0

    def userupdatesubject(self, username, subjectobj_t):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        subjects = userobj[1].get('subjects')
        if subjects is None:
            return -12
        else:
            assignedsub = subjects.get(subjectobj_t[0])
            if assignedsub is None:
                return -11
        userobj[1]['subjects'][subjectobj_t[0]] = {'content': subjectobj_t[1]}

        self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
        self.redis_pipe.execute()
        return 0

    def useraddsubject(self, username, subjectobj_t):
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        subjects = userobj[1].get('subjects')
        if subjects is None:
            userobj[1]['subjects'] = {}
        else:
            if subjectobj_t[0] in subjects.keys():
                if subjects.get(subjectobj_t[0]).get['isremoved'] is True:
                    return -12
                else:
                    return -11
        userobj[1]['subjects'][subjectobj_t[0]] = {'content': subjectobj_t[1]}

        self.redis_pipe.hset("sports:users", userobj[0], ujson.dumps(userobj[1]))
        self.redis_pipe.execute()
        return 0

    def getusersubjectscontent(self, username, isowner=False):
        """
        """
        print "============>",username
        userobj = self.__getuserobject(username)
        if type(userobj) == int:
            return userobj
        subjects = userobj[1].get('subjects')
        nickname = userobj[1].get('nickname')
        subs = {}
        if subjects is None:
            return (nickname, subs)
        else:
            if isowner:
                [subs.setdefault(s, v) for s, v in subjects.items() if v.get('isremoved') in [None, False]]
            else:
                [subs.setdefault(s, v) for s, v in subjects.items()\
                 if v.get('isremoved') in [None, False] or \
                 v.get('isclosed') in [None, False]]

        return (nickname, subs)

    def queryblocks(self, keys, serious=False):
        """
        """
        if keys is None or len(keys) == 0:
            return -1
        blocks = self.redis_server_admindb.smembers("sports:blocks")
        if blocks is None or len(blocks) == 0:
            return -2

        if serious:
            return [b for b in blocks if b.find(keys) == 0]
        return [b for b in blocks if b.find(keys) >= 0]

    def __getuserobject(self, username):
        if username is None:
            return -1
        try:
            umd5 = md5value(username)
            _tmp = self.redis_server.hget("sports:users", umd5)
            if _tmp is None:
                return -2
            uobj = ujson.loads(_tmp)
        except:
            return -3
        return (umd5, uobj)

    def getusernickname(self, username):
        uobj = self.__getuserobject(username)
        if type(uobj) == int:
            return uobj
        return uobj[1].get('nickname')

    def __getvaildprojectdata(self, projectkey):
        """
        """
        elem = projectkey.split("_")
        try:
            if len(elem) < 2:
                return -1
            onkey = '_'.join(elem[:2]+['on'])
            offkey = '_'.join(elem[:2]+['off'])
            _ontmp = self.redis_server.hget("sports:projects", onkey)
            _offtmp = self.redis_server.hget("sports:projects", offkey)
            print "=========>", onkey, offkey, _ontmp, _offtmp
            if _ontmp is None and _offtmp is None:
                return -2
            if _ontmp is None:
                _pobj = ujson.loads(_offtmp)
                pobj = _pobj['src']
                _retkey = self.__checkprojectkeyvalid(pobj['startdate'], offkey)
            else:
                _pobj = ujson.loads(_ontmp)
                pobj = _pobj['src']
                _retkey = self.__checkprojectkeyvalid(pobj['startdate'], onkey)

            if type(_retkey) == int or _retkey is None:
                    return -4
            print _retkey, pobj
            return (_retkey, pobj)
        except Exception as e:
            print traceback.print_exc()
            return -3

    def getprojectdetail(self, projectid):
        """
        """
        if projectid is None:
            return -1
        try:
            ret = self.__getvaildprojectdata(projectid)

            if type(ret) == int or ret[1] is None:
                return -2
            else:
                return ret
        except Exception as e:
            print traceback.print_exc()
            return -3

    def getuserprojectlist(self, username):
        if username is None:
            return -1
        umd5 = md5value(username)
        retdict = {'on': [], 'off': [], 'self': [], 'data': {}}
        sorteddate = []
        for projectkey in self.redis_server.smembers("sports:%s:projects"%umd5):
            if projectkey is not None:
                try:
                    _projectobj = self.__getvaildprojectdata(projectkey)
                    if type(_projectobj) == int or _projectobj[1] is None:
                        continue
                    _et = _projectobj[0].split("_")
                    print _et
                    projectobj = _projectobj[1]

                    elem = {'title': projectobj['title'], 'status': _et[-1],
                            'startdate': projectobj['startdate']}

                    if _et[0] == umd5:
                        elem['self'] = True
                        retdict['self'].append(_projectobj[0])

                    if _et[-1] == 'on':
                        retdict['on'].append(_projectobj[0])
                    if _et[-1] == 'off':
                        retdict['off'].append(_projectobj[0])
                    retdict['data'][_projectobj[0]] = elem
                    sorteddate.append((_projectobj[0], parse(projectobj['startdate'])))
                except Exception as e:
                    print e
                    print traceback.print_exc()
                    continue
        data = sorted(sorteddate, key=lambda k: k[1], reverse=True)
        retdict['sorted'] = data
        return retdict

    def checkprojectstatus(self, username, ptimestamp):
        """
        this need to change... unused now!!!  2015年 11月 04日 星期三 14:27:07 CST
        """
        umd5 = md5value(username)
        kflag = "%s_%s_on"%(umd5, ptimestamp)
        _tmp = self.redis_server.hget('sports:projects', kflag)
        if _tmp is None:
            return -11
        try:
            pobj = ujson.loads(_tmp)
            timegap = (parse(pobj['startdate'])-datetime.now()).total_seconds()
            if timegap >= 0:
                pobj['status'] = 0
            else:
                self.redis_pipe.hdel('sports:projects', kflag)
                self.redis_pipe.hset('sports:projects', "%s_%s_off"%(umd5, ptimestamp), _tmp)
                self.execute()
                pobj['status'] = -1
        except Exception as e:
            return -12
        return pobj['status']

    def __checkprojectkeyvalid(self, startdate, projectkey):
        if startdate is None or projectkey is None:
            return -1
        try:
            kelem = projectkey.split("_")
            if len(kelem) < 3:
                return -2
            status = kelem[2]
            needchangekey = -1
            retkey = projectkey

            if (datetime.now() - parse(startdate)).days <= 0:
                # project is on
                if status == "off":
                    needchangekey = 0
            else:
                # project is off
                needchangekey = 1

            if needchangekey != -1:
                project = self.redis_server.hget("sports:projects", projectkey)
                if needchangekey == 0:
                    # change key to on
                    newprojectkey = '_'.join(kelem[:2]+['on'])
                if needchangekey == 1:
                    newprojectkey = '_'.join(kelem[:2]+['off'])
                if projectkey != newprojectkey:
                    self.redis_pipe.hdel("sports:projects", projectkey)
                    self.redis_pipe.hset("sports:projects", newprojectkey, project)
                    self.redis_pipe.execute()
                retkey = newprojectkey
            return retkey
        except Exception as e:
            print e
            print traceback.print_exc()
            return -3

    def updateproject2db(self, projectkey, dictobj, username):
        """
        it use to update project info
        """
        if dictobj is None:
            return -1
        try:
            umd5 = md5value(username)
            retsrc = self.redis_server.hget("sports:projects", projectkey)
            retobj = ujson.loads(retsrc)
            retobj['src'] = dictobj
            _flagkey = self.__checkprojectkeyvalid(dictobj['startdate'], projectkey)
            if type(_flagkey) == int:
                return -3
            kflag = _flagkey
            self.redis_pipe.hset("sports:projects", kflag, ujson.dumps(retobj))
            self.redis_pipe.execute()
        except Exception as e:
            print traceback.print_exc()
            return -2
        return 0

    def removeprojectfromdb(self, projectkey):
        """
        """
        ret = self.__getvaildprojectdata(projectkey)
        if type(ret) == int:
            return -1
        keyid = ret[0]
        kinfo = projectkey.split("_")
        umd5 = kinfo[0]
        if umd5 is None:
            return -3
        if keyid is None:
            return -2
        # temp use for test data.
        self.redis_pipe.srem("sports:%s:projects"%umd5, projectkey+"_on")
        self.redis_pipe.srem("sports:%s:projects"%umd5, projectkey+"_off")

        self.redis_pipe.srem("sports:%s:projects"%umd5, projectkey)
        self.redis_pipe.hdel("sports:projects", keyid)
        self.redis_pipe.execute()
        return 0

    def addnewproject2db(self, dictobj, username):
        """
        """
        if dictobj is None:
            return -1
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            umd5 = md5value(username)
            kflag = "%s_%s_on"%(umd5, timestamp)
            ret = {'src': dictobj, 'author':username, 'joiner':[]}
            self.redis_pipe.hset("sports:projects", kflag, ujson.dumps(ret))
            self.redis_pipe.sadd("sports:%s:projects"%umd5, "%s_%s"%(umd5, timestamp))
            self.redis_pipe.execute()
        except Exception as e:
            return -2
        return 0


def main():
    """
    """
    sp = SocialDBProcessModule()
    sp.__userquerykey__()
  #  print sp.cleansubject('25422875@qq.com', u'足球')

if __name__ == '__main__':
    main()
