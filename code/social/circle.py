#  =========== coding:utf8 =============
from socialpublic import *


@route("/sports/personalsocial/circle")
def personalsocialcircle():
    """
    """
    uc = userbasicinfocheck()
    if type(uc) != tuple:
        return uc

    retciclelist = []
    return template("sports_personalsocial_circle", userinfo=uc[0], md5id=uc[1], circlelist=[])


@route("/sports/personalsocial/circle/publishnewarticle")
def circle_publishnewarticle():
    return template("sports_personalsocial_circle_publishnewarticle")


@route("/sports/personalsocial/circle/createcircle")
def circle_createcircle():
    return template("sports_personalsocial_circle_createnewcircle")


@route("/sports/personalsocial/addnewfriends", method="GET")
def circle_addnewfriends():
    t_circle = request.GET.get('type')
    if t_circle is None or t_circle == "":
        return abort(404)

    if t_circle != 'circle':
        return abort(404)

    flag = request.GET.get('flag')
    # flag is 0 : people can see, flag is 1 people can't see

    tosomeone = request.GET.get('to')
    if tosomeone is None or tosomeone == "":
        return abort(404)

    s = checkloginstatus()
    if type(s) != tuple:
        return s

    return template("addnewfriendmodual", flag=int(flag))


@route("/sports/personalsocial/circle/ajax_newcircle", method="POST")
def ajax_newcircle():
    circlename = request.POST.get('name')
    userlist = [k for k in request.POST.keys() if k not in [None, 'name']]

    print circlename, userlist

    ret = {'status': -1}
    if circlename == "" or circlename is None:
        return ret

    return ret


@route("/sports/personalsocial/circle/uploadarticle", method="POST")
def circle_uploadarticle():
    articleid = request.POST.get("articleid")
    iscontent = request.POST.get("iscontent")

    ret = {'status': -1, 'image': 0, 'content': 0}
    s = checkloginstatus()
    if type(s) != tuple:
        ret['status'] = -11
        return ret

    username = s[0]
    if iscontent is None or articleid is None:
        return ret
    dbelem = {'content': None, 'image': None}
    if iscontent.lower() == "true":
        content = request.POST.get("content")
        if content is None or content == "":
            ret['status'] = -4
            return ret
        dbelem['content'] = content

    elif iscontent.lower() == "false":
        imagebase64 = request.POST.get("imagebase64")
        if imagebase64 is None or imagebase64 == "":
            ret['status'] = -3
            return ret
        _f = savearticleimage(username, imagebase64)
        if type(_f) == int:
            ret['status'] = -3
            return ret
        dbelem['image'] = _f
    else:
        ret['status'] = -2
        return ret

    _f = SocialDB.updatearticleinfo(username, articleid, dbelem)
    if _f < 0:
        ret['status'] = -5
    else:
        ret['status'] = 0
    return ret
