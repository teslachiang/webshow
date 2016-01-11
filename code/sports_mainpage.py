# =========== coding:utf8 =============

from publicdefine import *


@bottle.route("/sports/mainpage")
def sports_mainpage():
    artlist = AdminArtDB.gethotarticles()
    username = None
    s = checkloginstatus()
    if type(s) == tuple:
        username = s[0]
    return template("sports_mainpagepage", articlelist=artlist, username=username)


@bottle.route("/sports/mainpage/article", method="GET")
def sports_mainpagegetarticle():
    artid = request.GET.get('id')
    username = None
    if artid is None or artid == "":
        return abort(404)
    retart = AdminArtDB.getarticlebyid(artid)
    if type(retart) == int:
        return abort(404)
    s = checkloginstatus()
    if type(s) == tuple:
        username = s[0]
    return template("sports_mainpage_article", artobj=retart, username=username)


@bottle.route("/sports/query", method="POST")
def sports_mainquery():
    ret = {'status': -1}
    q_type = request.POST.get('type')
    if q_type is None or q_type == "":
        return ret
    if q_type == "block":
        block = request.POST.get('block')
        # db get all block info
        ret['status'] = 0
    return ret
