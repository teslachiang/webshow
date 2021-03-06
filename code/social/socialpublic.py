# ========== coding:utf8 =========
from publicdefine import *
from personalsocial_DBModule import SocialDBProcessModule

SocialDB = SocialDBProcessModule()


def getuserprovidesubjects(username, isowner=False):
    """
    """
    subs = SocialDB.getusersubjectscontent(username, isowner=isowner)

    if type(subs) != tuple:
        return abort(500, type(subs))
    (nickname, usersubjects) = subs
    if type(usersubjects) == int:
        return abort(500)
    if nickname is None:
        nickname = username

    students = 0
    subjectlist = []

    for sub, subobj in usersubjects.items():
        members = 0
        if subobj.get('members') is not None:
            members = len(subobj.get('members'))
        isclosed = subobj.get('isclosed')
        if isclosed is None:
            isclosed = False
        subjectlist.append((sub, members, isclosed))
        students += members
    return template("sports_personalsocial_providesubject",
                    username=username, nickname=nickname,
                    subjectlist=subjectlist, students=students)
