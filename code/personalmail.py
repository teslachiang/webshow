#  =========== coding:utf8 =============


from publicdefine import *


@bottle.route("/sports/personalmail/mainpage")
def mailmainpage():
    """
    """
    uc = userbasicinfocheck()
    if type(uc) != tuple:
        return uc
    return template('sports_personalmail_mainpage', userinfo=uc[0], md5id=uc[1])


@bottle.route("/sports/personalmail/inboxpage")
def name():
    """
    """
    inmail = {'001': {'from':'28422575@qq.com', 'title': '亚马逊订单提醒', 'date': '2015-10-15 07:05:01'},
              '002': {'from':'28422575@qq.com', 'title': '广告提醒', 'date': '2015-11-15 07:05:01'},
              '003': {'from':'28422575@qq.com', 'title': '索尼活动羽毛球', 'date': '2015-10-25 07:05:01'},
              '004': {'from':'28422575@qq.com', 'title': '虎妞申请教授科目羽毛球', 'date': '2015-06-05 07:05:01'}}
    return template('mail_inboxpage', itemlist=inmail)


@bottle.route("/sports/personalmail/sendboxpage")
def name():
    """
    """
    return template('mail_sendboxpage')


@bottle.route("/sports/personalmail/trashboxpage")
def name():
    """
    """
    return template('mail_trashboxpage')


@bottle.route("/sports/personalmail/mailbox", method="GET")
def checkmail():
    boxtype = request.GET.get('boxtype')
    mailid = request.GET.get('mailid')

    return template('sports_personalmail_mailview')


@bottle.route("/sports/personalmail/reply", method="GET")
def processmail():
    reply_type = request.GET.get('type')
    mailid = request.GET.get('mailid')
    # reply type 0 is reply, 1 is reply to all , -1 is forward    
    return template('sports_personalmail_mailreply')
