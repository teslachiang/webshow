#  =========== coding:utf8 =============
from socialpublic import *


@route("/sports/personalsocial")
def personalsocial():
    """
    """
    # s = checkloginstatus()
    # if type(s) != tuple:
    #     return s
    # username = s[0]
    # nickname = SocialDB.getusernickname(username)
    return userbasicinfo_response("sports_personalsocialpage")
#    return template("sports_personalsocialpage", username=username, nickname=nickname)


@route("/sports/personalsocial/schedule")
def personalsocialschedule():
    """
    """
    uc = userbasicinfocheck()
    if type(uc) != tuple:
        return uc

    ret = SocialDB.getuserprojectlist(uc[0]['username'])

    if type(ret) == int:
        return abort(500, "error code:"+ret)

    return template("sports_personalsocial_schedule", obj=ret, userinfo=uc[0], md5id=uc[1])


@route("/sports/personalsocial/taskdetail", method="GET")
def personalsocialchedule_taskdetail():
    taskkey = request.GET.get('key')
    if taskkey is None:
        return abort(404)
    s = checkloginstatus()
    if type(s) != tuple:
        return s
    umd5 = md5value(s[0])
    owner = False
    if taskkey.find(umd5) >= 0:
        owner = True
    taskobj = SocialDB.getprojectdetail(taskkey)
    if type(taskobj) == int or taskobj is None:
        return abort(500, "please check it, get db error:%s"%taskobj)
    print taskobj    
    return template("sports_personalsocial_taskdetail", taskid=taskkey, taskobj=taskobj[1], owner=owner)


@route("/sports/personalsocial/removegame", method="POST")
def personalsocialsremovegame():
    taskkey = request.POST.get('key')
    ret = {'status': -1}
    if taskkey is None:
        return ret
    s = checkloginstatus()
    if type(s) != tuple:
        ret['status'] = -2
        return ret
    umd5 = md5value(s[0])
    owner = False
    if taskkey.find(umd5) >= 0:
        owner = True
        sret = SocialDB.removeprojectfromdb(taskkey)
        if sret < 0:
            ret['status'] = -4
            return ret
        ret['status'] = 0
        return ret
    else:
        ret['status'] = -3
        return ret


@route("/sports/personalsocial/editgame", method="GET")
def personalsocialseditgame():
    taskkey = request.GET.get('key')
    if taskkey is None:
        return abort(404)
    s = checkloginstatus()
    if type(s) != tuple:
        return s
    umd5 = md5value(s[0])
    owner = False
    if taskkey.find(umd5) >= 0:
        owner = True
        taskobj = SocialDB.getprojectdetail(taskkey)
    else:
        return abort(500, "your have no right update the project")
    if type(taskobj) == int or taskobj[1] is None:
        return abort(500, "please check it, get db error:%s"%taskobj[0])
    return template("sports_personalsocial_editgame", projectkey=taskobj[0], taskobj=taskobj[1])


@route("/sports/personalsocial/addgame")
def personalsocialsaddgame():
    """
    """
    s = checkloginstatus()
    if type(s) != tuple:
        return s
    return template("sports_personalsocial_addgame")


@route("/sports/personalsocial/modifygameajax", method="POST")
def personalsocialscreategame():
    """
    """
    tasktitle = request.POST.get('tasktitle')
    start = request.POST.get('start')
    cost = request.POST.get('cost')
    tstart = request.POST.get('tstart')
    tend = request.POST.get('tend')
    descript = request.POST.get('descript')
    address = request.POST.get('address')
    projectkey = request.POST.get('projectkey')
    ret = {'status': -1}
    if tasktitle is None or descript is None or address is None:
        return ret
    s = checkloginstatus()
    if type(s) != tuple:
        ret['status'] = -2
        return ret
    projectobj = {'title': tasktitle, 'startdate': start, 'cost': cost,
                  'startenter': tstart, 'endenter': tend, 'descript': descript,
                  'address': address}
    if projectkey is None or projectkey == "":
        flag = SocialDB.addnewproject2db(projectobj, s[0])
    else:
        flag = SocialDB.updateproject2db(projectkey, projectobj, s[0])
    if flag < 0:
        ret['status'] = -3
        ret['flag'] = flag
    else:
        ret['status'] = 0

    return ret


@route("/sports/personalsocial/userprovidesubject", method="GET")
def personalsocial_userprovidesubject():
    """
    """
    username = request.GET.get('username')
    if username is None or username == "":
        return abort(404)

    return htmluserprovidesubjects(username)


@route("/sports/personalsocial/toggleprovidesubject", method="GET")
def personalsocial_toggleprovidesubject():
    username = request.GET.get('username')
    subject = request.GET.get('subject')
    _isclose = request.GET.get('isclose')

    if username is None or username == "":
        return abort(404)
    if subject is None or subject == "":
        return abort(404)
    if _isclose is None or _isclose == "":
        return abort(404)
    if _isclose == "0":
        isclosed = False
    else:
        isclosed = True

    s = checkloginstatus()
    if type(s) != tuple:
        return s

    if username == s[0]:
        flag = SocialDB.usertogglesuject(username, subject.decode("utf8"), isclose=isclosed)
        if flag < 0:
            return abort(500, "error:%s"%flag)
        return redirect("/sports/personalsocial/providesubject")
    else:
        abort(500, "no right access")


@route("/sports/personalsocial/providesubject")
def personalsocial_providesubject():
    s = checkloginstatus()
    if type(s) != tuple:
        return s
    username = s[0]
    return getuserprovidesubjects(username, isowner=True)


@route("/sports/personalsocial/queryblockajax", method="POST")
def personalsocial_queryblockajax():
    key = request.POST.get('key')
    ret = {'status': -1}
    if key is None:
        return ret

    qret = SocialDB.queryblocks(key)

    if type(qret) == int:
        ret['status'] = -2
        return ret
    else:
        ret['status'] = 0
        ret['data'] = qret
    return ret


@route("/sports/personalsocial/checksubjectdetail", method="GET")
def personalsocial_checksubjectdetail():
    username = request.GET.get('user')
    subject = request.GET.get('subject')

    if username is None or username == "":
        return abort(404)
    if subject is None or subject == "":
        return abort(404)

    (nickname, subjectdict) = SocialDB.getusersubjects(username)

    sub = subjectdict.get(subject.decode("utf8"))
    if sub is None:
        return abort(404)
    subjectisclosed = sub.get('isclosed')
    print sub
    if subjectisclosed is None:
        subjectisclosed = False
    students = sub.get('members')
    if students is None:
        students = []
    if nickname is None:
        nickname = username

    isowner = False
    s = checkloginstatus()

    if type(s) != tuple:
        isowner = False
    if username == s[0]:
        isowner = True

    return template("sports_personalsocial_subjectdetail", username=username,
                    nickname=nickname, subject=subject, subjectcontent=sub['content'],
                    students=students, owner=isowner, isclosed=subjectisclosed, comments=10)


@route("/sports/personalsocial/editsubject", method="GET")
def personalsocial_editsubject():
    username = request.GET.get('username')
    subject = request.GET.get('subject')

    print __name__, username, subject
    if username is None or username == "":
        return abort(404)
    if subject is None or subject == "":
        return abort(404)

    s = checkloginstatus()
    if type(s) != tuple:
        return s
    if username != s[0]:
        return redirect('/sports/login')

    (nickname, subjectdict) = SocialDB.getusersubjects(username)

    sub = subjectdict.get(subject.decode("utf8"))
    if sub is None:
        return abort(404)

    return template("sports_personalsocial_editprovidesubject", subjectcontent=sub['content'], subject=subject)


@route("/sports/personalsocial/removesubjectajax", method="POST")
def personalsocial_removesubjectajax():
    username = request.POST.get('username')
    subject = request.POST.get('subject')

    ret = {'status': -1}
    if subject is None or username is None:
        return ret

    s = checkloginstatus()
    if type(s) != tuple:
        ret['status'] = -2
        return ret

    if username != s[0]:
        ret['status'] = -3
        return ret
    else:
        # remove subject!!
        _flag = SocialDB.userremovesuject(username, subject.decode("utf8"))
        if _flag == 0:
            ret['status'] = 0
        else:
            ret['status'] = -4
            print "db process error1!!!", _flag
        return ret


@route("/sports/personalsocial/submitsubjectajax", method="POST")
def personalsocial_submitsubjectajax():
    subject = request.POST.get('subject')
    descript = request.POST.get("descript")
    isupdate = request.POST.get('isupdate')

    ret = {'status': -1}
    if subject is None or descript is None:
        return ret

    s = checkloginstatus()
    if type(s) != tuple:
        ret['status'] = -2
        return ret

    username = s[0]
    print subject, descript
    qret = SocialDB.queryblocks(subject, serious=True)

    if type(qret) == int or len(qret) == 0:
        ret['status'] = -3
        return ret

    # write 2 db
    subjectobj = (subject.decode('utf8'), descript)
    if isupdate == "1":
        print 'updatesubject info!!!!'
        retadd = SocialDB.userupdatesubject(username, subjectobj)
    else:
        retadd = SocialDB.useraddsubject(username, subjectobj)

    print retadd
    if retadd < 0:
        ret['status'] = -4
        ret['flag'] = retadd
    else:
        ret['status'] = 0
    return ret


@route("/sports/personalsocial/addprovidesubject")
def personalsocial_addprovidesubject():
    """
    """
    s = checkloginstatus()
    if type(s) != tuple:
        return s
    return template("sports_personalsocial_addprovidesubject")



@route("/sports/personalsocial/circlecreate")
def personalsocialcirclecreate():
    """
    """
    return template("sports_personalsocial_circlecreate")


@route("/sports/personalsocial/circlesearch")
def personalsocialcirclesearch():
    """
    """
    return template("sports_personalsocial_circlesearch")
