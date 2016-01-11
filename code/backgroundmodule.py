# ===========coding:utf8============
from publicdefine import *


@bottle.route("/sports/background/signin")
def background_signin():
    """
    """
    return template("background_signin")


@bottle.route("/sports/background/signedframepage", method="GET")
def background_framepage():
    """
    """
    email = request.GET.get('email')
    password = request.GET.get('password')
    pagetype = request.GET.get("pagetype")
    curpage = request.GET.get("curpage")

    if email is None or password is None:
        return abort(404)

    if type(db.dbcheckuser(email, password, pwmd5=True)) == int:
        return abort(500, 'you have no right to access the link, please login!')
    flag = False
    arts = db.dbadmingetarticles(email)
    artlen = len(arts)
    print type(arts)
    print pagetype, curpage
    if pagetype is None:
        arts = arts[:10]
    else:
        if curpage is None:
            return abort(404)
        try:
            cindex = int(curpage)
            if pagetype == 'pre':
                if cindex <= 10:
                    arts = arts[:10]
                else:
                    arts = arts[cindex-10:cindex]
            if pagetype == 'next':
                if (cindex + 10)>=len(arts):
                    arts = arts[cindex:]
                else:
                    arts = arts[cindex:cindex+10]
        except Exception as e:
            print e
            print traceback.print_exc()
            return abort(500, "article query error!!")

    return template("background_userarticles", articles=arts, artlen=artlen, email=email, password=password)


@bottle.route("/sports/background/modifyarticle", method="GET")
def background_modifyarticle():
    artid = request.GET.get('artid')
    email = request.GET.get('email')
    password = request.GET.get('password')

    if artid is None or email is None or password is None:
        return abort(404)
    if type(db.dbcheckuser(email, password, pwmd5=True)) == int:
        return abort(500, 'you have no right to access the link, please login!')

    artobj = db.dbgetadminarticle(artid)
    if type(artobj) == int:
        print "get article error====>", artobj
        return abort(404)

    return template('background_modifyarticle', email=email,
                    username=email.split("@")[0],
                    article=artobj)


@bottle.route("/sports/background/removearticle", method="POST")
def background_removearticle():
    artid = request.POST.get('artid')
    email = request.POST.get('email')
    password = request.POST.get('password')
    ret = {'status': -1}

    if artid is None or email is None or password is None:
        return ret
    if type(db.dbcheckuser(email, password, pwmd5=True)) == int:
        ret['status'] = -2
        return ret
    f = db.dbadminremovearticle(email, artid)
    print "--->", f
    if f == 0:
        ret['status'] = 0
    else:
        ret['status'] = -3
    return ret


@bottle.route("/sports/background/checkarticle", method="GET")
def background_checkarticle():
    artid = request.GET.get('artid')
    email = request.GET.get('email')
    password = request.GET.get('password')

    if artid is None or email is None or password is None:
        return abort(404)
    if type(db.dbcheckuser(email, password, pwmd5=True)) == int:
        return abort(500, 'no right access this page, please login')
    artobj = db.dbgetadminarticle(artid)
    if type(artobj) == int:
        print "get article error====>", artobj
        return abort(404)
    return template('background_articlepreview', article=artobj)


@bottle.route("/sports/background/ajaxqueryblock", method="POST")
def background_ajaxqueryblock():
    keyword = request.POST.get("keyword")
    print request.POST.items()
    ret = {'status': -1}
    print "keyword", keyword
    if keyword is None or len(keyword) == 0:
        return ret
    queryret = db.queryblocks(keyword)
    ret['status'] = 0
    ret['result'] = list(queryret)
    return ret


@bottle.route("/sports/background/uploadimages", method="POST")
def background_uploadimages():
    upload = request.files.get('upfile')
    username = request.POST.get("username")
    timestamp = datetime.now().strftime("%Y%m%d-%H-%M-%S")
    ret = {"status": -1, 'imglink': "/static/%s_%s_%s"}
    if upload:
        print 'ready to save image'
        try:
            imageupload = os.path.join(curdir, "static/%s_%s_%s"%(username, timestamp, upload.filename))
            if os.path.exists(imageupload) is False:
                upload.save(imageupload)
            ret['status'] = 0
            ret['imglink'] = ret['imglink']%(username, timestamp, upload.filename)
        except Exception as e:
                print e
    return ujson.dumps(ret)


@bottle.route("/sports/background/searcharticles", method="POST")
def searcharticles():
    keyword = request.POST.get('keyword')
    email = request.POST.get('email')
    password = request.POST.get('password')

    ret = {'status': -1}
    print 'keyword:---->', keyword
    if keyword is None or email is None or password is None:
        return ret
    if type(db.dbcheckuser(email, password, pwmd5=True)) == int:
        ret['status'] = -4
        return ret
    # check search type
    queryblock = None
    titlekey = None
    if keyword.strip().find("+") >= 0:
        _tmp = keyword.split("+")
        if len(_tmp) < 2:
            ret['status'] = -2
            return ret
        titlekey = _tmp[0]
        blockkey = _tmp[1]

        if blockkey in [None, ""]:
            queryblock = db.queryblocks("*")
        else:
            queryblock = db.queryblocks(blockkey)
    else:
        # easy search
        queryblock = db.queryblocks("*")
        titlekey = keyword.strip()

    if queryblock is None or len(queryblock) == 0:
        ret['status'] = 0
        return ret
    result = []
    for b in queryblock:
        bf = db.dbqueryblockarticles(email, b.decode("utf8"), titlekey.decode("utf8"))
        print bf
        if type(bf) == int:
            ret['status'] = -3
            return ret
        result.extend(bf)
    if len(result) == 0:
        ret['status'] = 0
        return ret
    ret['status'] = 1
    ret['result'] = result
    return ret


@bottle.route("/sports/background/submitarticlemodify", method="POST")
def submitarticlemodify():
    """
    """
    title = request.POST.get('title')
    block = request.POST.get('block')
    tags = request.POST.get('tags')
    email = request.POST.get('email')
    content = request.POST.get('content')
    artid = request.POST.get('artid')
    timestamp = request.POST.get('timestamp')
    print title, block, tags, email, artid

    ret = {'status': -1}
    if email is None or artid is None or timestamp is None:
        return ret
    if title is None or block is None or tags is None or content is None:
        ret['status'] = -2
        return ret

    if block.strip() not in db.queryblocks("*"):
        ret['status'] = -3
        return ret

    _content = checkarticlevalid(content, articleid=artid)
    if type(_content) == int:
        ret['status'] = -4
        return ret
    content = _content

    # ready to save to db
    artobj = {'title': title, 'block': block,
              'tags': tags, 'content': content,
              'author': email,
              'timestamp': timestamp,
              'modify_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              'articleid': artid}
    r = db.dbadminmodifyarticle(email, artid, artobj)
    print "--------------r>", r
    if r < 0:
        ret['status'] = -5
        return ret
    ret['status'] = 0
    return ret


@bottle.route("/sports/background/submitarticle", method="POST")
def background_submitarticle():
    title = request.POST.get('title')
    block = request.POST.get('block')
    tags = request.POST.get('tags')
    email = request.POST.get('email')
    content = request.POST.get('content')

    print title, block, tags, content, email

    ret = {'status': -1}
    if email is None:
        return ret
    if title is None or block is None or tags is None or content is None:
        ret['status'] = -2
        return ret

    if block.strip() not in db.queryblocks("*"):
        ret['status'] = -3
        return ret
    # create article id
    artid = db.createarticleid()
    _content = checkarticlevalid(content, articleid=artid)
    if type(_content) == int:
        ret['status'] = -4
        return ret
    content = _content

    # ready to save to db
    artobj = {'title': title, 'block': block,
              'tags': tags, 'content': content,
              'author': email,
              'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              'articleid': artid}
    r = db.dbadminaddarticle(email, artobj)
    if r < 0:
        ret['status'] = -5
        return ret
    ret['status'] = 0
    return ret


@bottle.route("/sports/background/signed", method="POST")
def background_signin_post():
    """
    """
    email = request.POST.get('useremail')
    password = request.POST.get('password')
    rememberme = request.POST.get('rememberme')

    if email is None or password is None:
        return abort(404)

    s = bottle.request.environ.get('beaker.session')
    s['email'] = (email, md5value(password))
    s.save()

    # check user info
    ret = db.dbcheckuser(email, password)
    if type(ret) == int:
        return redirect("/sports/background/signin")

    if rememberme is None:
        s = bottle.request.environ.get('beaker.session')
        s['email'] = None
        s.save()

    return template("background_userinputinfo",
                    email=email, password=md5value(password),
                    username=email.split("@")[0], articles=ret['articles'])
