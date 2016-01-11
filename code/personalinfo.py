# =========== coding:utf8 =============

from publicdefine import *
from imagecropper import processimgcrop

UDBProcess = RPDB


def personalinfobasic_response(password, username, md5id):
    if username is None or password is None:
        return abort(500, "access denied!!")
    f = UDBProcess.checkuserinvalid(username.strip(), password)
    if f == 0:
        userobj = UDBProcess.dbgetuserinfo(regname=username.strip())
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

        return template("sports_personalinfo_basic", userinfo=userobj, md5id=md5id)
    else:
        return abort(500, "access denied!!")


@bottle.route("/sports/personalinfo/basic")
def personalinfobasic():
    s = checkloginstatus()

    if type(s) != tuple:
        return s

    password = s[1]
    username = s[0]

    return personalinfobasic_response(password, username, md5id=md5value(username))


@bottle.route("/sports/personalinfo/quitaccount")
def personalinfo_quitaccount():
    """
    """
    try:
        s = bottle.request.environ.get('beaker.session')
        s.invalidate()
    except:
        pass
    finally:
        return redirect("/sports/mainpage")


@bottle.route("/sports/personalinfo/basic", method="POST")
def personalinfobasicpost():
    """
    """
    username = request.POST.get("username")
    password = request.POST.get("password")

    return personalinfobasic_response(password, username, md5id=md5value(username))


@bottle.route("/sports/personalinfo/basic/updatepersonalinfo", method="POST")
def updatepersonalinfo():
    """
    """
    msgtype = request.POST.get('msgtype')
    postdata = request.POST.get('dataobj')
    username = request.POST.get("username")
    print request.POST.items()
    print "--->", postdata
    ret = {'status': -1}
    if msgtype is None or len(msgtype) == 0 or username is None:
        return ret

    elem = {'username': None, 'nickname': None,
            'sex': None, 'words': None,
            'contact': {'name': None, "phonenumber": None, 'address': None},
            'area': None
            }

    if postdata is None and msgtype != 'contact':
        ret['status'] = -2
        return ret

    if msgtype == 'contact':
        try:
            dataobj = ujson.loads(postdata)
            name = dataobj['name']
            phonenumber = dataobj['phonenumber']
            address = dataobj['address']
            ret['status'] = 0
            elem['contact']['name'] = name
            elem['contact']['phonenumber'] = phonenumber
            elem['contact']['address'] = address
        except Exception as e:
            ret['status'] = -11
            return ret

    if msgtype == 'sex':
        if len(postdata.strip()) > 0:
            ret['status'] = 0
            elem['sex'] = postdata.strip()

    if msgtype == 'area':
        if len(postdata.strip()) > 0:
            city = postdata.split()[0]
            f = UDBProcess.checkcityvaild(city)
            print f
            if f != 0:
                ret['status'] = -3
                ret['code'] = f
            else:
                ret['status'] = 0
                elem['area'] = city  # postdata.strip()
    if msgtype == 'nickname':
        if len(postdata.strip()) > 0:
            ret['status'] = 0
            elem['nickname'] = postdata.strip()
    if msgtype == 'words':
        if len(postdata.strip()) > 0:
            ret['status'] = 0
            elem['words'] = postdata.strip()

    if ret['status'] == 0:
        f = UDBProcess.dbupdateuserinfo(elem, md5id=md5value(username))
        if f != 0:
            ret['status'] = -5
        print f

    return ret


@bottle.route("/sports/personalinfo/basic/querycityinfo", method="POST")
def querycityinfo():
    """
    """
    keywords = request.POST.get('keywords')
    ret = {'status': -1}
    if keywords is None or len(keywords.strip()) == 0:
        return ret
    r = UDBProcess.querycityinfo(keywords.strip())
    if type(r) == int:
        ret['status'] = -2
        ret['errorcode'] = r
    else:
        if len(r) == 0:
            ret['status'] = -3
        else:
            ret['status'] = 0
            ret['data'] = r
    return ret


@bottle.route("/sports/personalinfo/basic/uploadshortcut", method="POST")
def uploadshortcut():
    """
    """
    imgbase = request.POST.get('imgBase64')
    username = request.POST.get('usermd5')
    ret = {'status': 'error'}

    if imgbase is None or username is None:
        return ujson.dumps(ret)
    md5id = md5value(username)
    if imgbase:
        try:
            _imgbase = imgbase.split(",")
            _imgtype = _imgbase[0].split(";")[0]
            imgtype = _imgtype[_imgtype.rfind("/")+1:]
            imageupload = os.path.join(pardir, "static/headshortcut/")
            with open(os.path.join(imageupload, md5id+"_headcut.%s"%imgtype), "wb") as imgfh:
                imgfh.write(_imgbase[1].decode('base64'))
            # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # imagetype = upload.filename[upload.filename.rfind("."):]
            # tmpimgname = "%s_%s%s"%(md5id, timestamp, imagetype)
            # tmpimagepath = os.path.join(imageupload, tmpimgname)
            # if os.path.exists(tmpimagepath) is False:
            #     upload.save(tmpimagepath)
            # else:
            #     os.remove(tmpimagepath)
            #     upload.save(tmpimagepath)
            # cdata = {'x': request.POST.get('x'), 'y': request.POST.get('y'),
            #          'rotate': request.POST.get('rotate'),
            #          'width': request.POST.get('width'),
            #          'height': request.POST.get('height')}
            # ret = processimgcrop(imageupload, tmpimgname, cdata, md5id)
            # print ret, type(ret)
            # if type(ret) != int:
            return ujson.dumps({"status": 'ok', 'imglink': "/static/headshortcut/%s"%md5id+"_headcut.%s"%imgtype})
            # else:
            #     raise Exception("process image error!!")
        except Exception as e:
            print e
            print traceback.print_exc()
            return ujson.dumps({"status": 'error', 'msg': "server error!"})
    else:
        print 'upload is none!!'
        return json.dumps({"status": 'error', 'msg': 'file handle is None'})
