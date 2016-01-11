#  =========== coding:utf8 =============
from publicdefine import *
from sports_articleDBModule import ArticleDBModule

adb = ArticleDBModule()


@bottle.route("/sports/personalarticle/mainpage")
def articlemainpage():
    """
    """
    uc = userbasicinfocheck()
    if type(uc) != tuple:
        return uc
    return template('sports_personalarticle_mainpage', userinfo=uc[0], md5id=uc[1])


@bottle.route("/sports/personalarticle/selectarticletype")
def selectarticletype():
    itemlist = ["篮球", "足球", "羽毛球", "跑步"]
    sptypes = adb.getsportstypes()
    if type(sptypes) == int:
        return abort(400, "sport load type error!!")
    return template("sports_selectarticletype", itemlist=itemlist, sporttypes=sptypes)


@bottle.route("/sports/personalarticle/myarticle")
def myarticlepage():
    """
    """
    return template('sports_personalarticle_myarticle')
