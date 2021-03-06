# ============== coding:utf8 ===============
import os
import sys
import redis
import ujson
import traceback
import hashlib
import re
import string
import bottle
import ConfigParser
import Cookie
from pyquery import PyQuery as pq
from dateutil.parser import parse
from datetime import datetime
from bottle import static_file, request, redirect, template, run, error, abort, route

reload(sys)
sys.setdefaultencoding("utf8")

filepath = os.path.abspath(os.path.realpath(__file__))
curdir = os.path.dirname(filepath)
pardir = '/'.join(curdir.split("/")[:-1])
re_localimg = re.compile("localhost:9011/static/(.+\.jpg|png|jpeg|gif)")

sys.path.append(os.path.join(curdir, 'social'))

bottle.TEMPLATE_PATH.append(pardir+"/template")
bottle.TEMPLATE_PATH.append(pardir+"/template/homepage")
bottle.TEMPLATE_PATH.append(pardir+"/template/background")
bottle.TEMPLATE_PATH.append(pardir+"/template/personalarticle")
bottle.TEMPLATE_PATH.append(pardir+"/template/personalinfo")
bottle.TEMPLATE_PATH.append(pardir+"/template/personalsocial")
bottle.TEMPLATE_PATH.append(pardir+"/template/personalmail")
bottle.TEMPLATE_PATH.append(pardir+"/template/usersign")


def timecost(func):
    def warpper(*args, **argv):
        """
        """
        start = datetime.now()
        func(*args, **argv)
        end = datetime.now()
        print '%s cost %s s'%(func.__name__, (end-start).seconds)
    return warpper


def stringfiltersymbol(instr):
    """
    """
    if instr is None:
        return
    regex = re.compile('[%s]'%re.escape(string.punctuation + u"：、[]『』（）？“”——， 《》"))
    return regex.sub("", instr.strip())


def md5value(instring):
    """
    """
    if instring is None:
        return
    md5 = hashlib.md5(instring.encode("utf8"))
    return md5.hexdigest()


# ============ session ==============
from beaker.middleware import SessionMiddleware
session_opts = {
       'session.type': 'file',
       'session.cookie_expires': 30000,
       'session.data_dir': curdir+'/data',
       'session.auto': True
}

# ========== db module initial ==============
from dbprocessmodule import DBProcessModule
from userdbprocessmodule import UserDBProcessModule
db = DBProcessModule()
AdminArtDB = db
RPDB = UserDBProcessModule()


def checkloginstatus():
    try:
        s = request.environ.get('beaker.session')
        username = s.get('username')
        password = s.get('password')
        if username is None or password is None:
            return redirect("/sports/login")
        else:
            return (username, password)
    except Cookie.CookieError as e:
        return redirect("/sports/login")


def userbasicinfocheck():
    s = checkloginstatus()
    if type(s) != tuple:
        return s
    username = s[0]
    password = s[1]
    if username is None or password is None:
        return redirect("/sports/login")
    md5id = md5value(username)
    userobj = RPDB.dbgetuserinfo(regname=username.strip())
    if type(userobj) == int:
        return abort(500, "system error! code:"+userobj)
    flag = None

    if md5id is not None:
        for k in ['.jpg', '.jpeg', '.png']:
            headcut = os.path.join(pardir, "static/headshortcut/%s_headcut%s"%(md5id, k))
            if os.path.exists(headcut) is True:
                flag = "/static/headshortcut/%s_headcut%s"%(md5id, k)
                break
    if flag is None:
        userobj['shortcut'] = "/static/headshortcut/default.png"
    else:
        userobj['shortcut'] = flag

    if userobj.get('nickname') is None:
        userobj['nickname'] = 'supername_001'

    return (userobj, md5id)


def userbasicinfo_response(templatename):
    uc = userbasicinfocheck()
    if type(uc) != tuple:
        return uc
    return template(templatename, userinfo=uc[0], md5id=uc[1])


def checkarticlevalid(content, host="localhost:9011", articleid=0):
    """
    """
    if content is None:
        return -1
    try:
        if len(pq(content).text()) < 50:
            return -2
        else:
            # check image link and add useful tag
            for img in pq(content)("img"):
                s = pq(img).attr('src')
                if s.find("http://") < 0 or s.find(host+"/static") >= 0:
                    if s.find("articleid(") < 0:
                        print "-------find img-------"
                        #  need to add article id
                        imgfile = re_localimg.findall(s)
                        if os.path.exists(os.path.join(curdir, "static/%s"%imgfile[0])):
                            os.rename(os.path.join(curdir, "static/%s"%imgfile[0]),
                                  os.path.join(curdir, "static/articleid(%s)_%s"%(articleid, imgfile[0])))

                            content = content.replace(pq(img).attr("src"),
                                                      "/static/articleid(%s)_%s"%(articleid, imgfile[0]))
            return content
    except Exception as e:
        print e
        return -4
