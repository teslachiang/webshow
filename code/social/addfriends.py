#  =========== coding:utf8 =============
from socialpublic import *


@route("/sports/personalsocial/addnewfriend")
def personalsocial_addnewfriend():
    return template("addnewfriend")


@route("/sports/personalsocial/friendlist")
def personalsocial_friendlist():
    """
    """
    return template("sports_personalsocial_friendlist")


@route("/sports/personalsocial/ajaxuserquery", method="POST")
def personalsocial_ajaxuserquery():
    keyword = request.POST.get('keyword')

    ret = {'status': -1}
    if keyword is None or keyword == "":
        return ret

    return ret
