#  =========== coding:utf8 =============
'''
    this module is for plateform register module
'''

from publicdefine import *
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from imagecropper import createuserqrcodecard
import random
import PIL

fontpath = "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf"

import Cookie


# def get_cookies():
#     ans = Cookie.SimpleCookie()
#     print "---->", ans
#     for b in bottle.request.environ.get("beaker.session", ";"):
#         try:
#             ans.load(b)
#         except Cookie.CookieError:
#             pass
#     return ans


def createcheckcode():
    """
    """
    try:
        checkwords = ujson.load(open(os.path.join(pardir, "static/checkcode/checkwords.json")))
        keys = [k for k, v in checkwords.items() if type(v) is not int]
        ri = random.randint(0, len(keys)-1)
        nimg = md5value("sn_%s_sn"%((ri+1)%7+1))
        print "number is :", (ri+1)%7+1
        print "number image is:", nimg
        print "word is: ", checkwords[keys[ri]]
        print "word image is", keys[ri]
        if nimg is None:
            raise Exception('parameter is NULL')
        return (nimg, keys[ri])
    except Exception as e:
        print e
        print traceback.print_exc()
        return


def verifycheckcode(inputstr, md5checkcode, md5number):
    """
    """
    if inputstr is None:
        return False

    if len(inputstr.strip()) < 2:
        return False
    try:
        obj = ujson.load(open(os.path.join(pardir, "static/checkcode/checkwords.json")))
        flag = -1
        targetword = obj[md5checkcode]
        print "input string is:", inputstr
        print "md5 checkcode is:", md5checkcode
        print "md5number is:", md5number
        print "targetword====>", targetword
        print "targetnumber====>", obj[md5number]
        flag = obj[md5number]-1

        correctword = None
        if flag == 0:
            correctword = targetword[:2]
        elif flag == 6:
            correctword = targetword[-2:]
        else:
            correctword = targetword[flag-1:flag+2]
        print "--->correct", correctword, flag, targetword, inputstr
        print "result: left :", inputstr.strip().lower(), "right:", correctword 
        print inputstr.strip().lower() == correctword
        if inputstr.strip().lower() == correctword:
            return True
        else:
            return False
    except Exception as e:
        print e
        return False


def createcheckcodeimglist():
    ret = {}
    checkwords = ['arising', 'framing', 'joiners', 'layover',
                  'lessons', 'lasting', 'marcher', 'accends',
                  'accinge', 'accited', 'accites', 'accloys',
                  'accoast', 'accoied', 'accoils', 'accompt',
                  'accourt', 'accoyed']
    for ri in range(7):
        imagenumber = Image.new("RGBA", (50,50), (255,255,255))
        drawn = ImageDraw.Draw(imagenumber)
        fontn = ImageFont.truetype(fontpath, 40)
        drawn.text((0, 0), '%s'%(ri+1), (183,50,44), font=fontn)
        md5file = md5value("sn_%s_sn"%(ri+1))
        img_resizedn = imagenumber.resize((20, 25), Image.ANTIALIAS)
        img_resizedn.save(os.path.join(pardir, "static/checkcode/%s_number.png"%md5file))
        ret[md5file] = ri+1

    for word in checkwords:
        image = Image.open(os.path.join(pardir, "static/checkcode/checkcode_background.jpg"))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(fontpath, 50)
        draw.text((10, 0), word, (17, 13, 157), font=font)
        img_resized = image.resize((188, 45), Image.ANTIALIAS)
        md5file = md5value("sp_%s_sp"%word)
        ret[md5file] = word
        img_resized.save(os.path.join(pardir, "static/checkcode/%s.png"%md5file))

    ujson.dump(ret, open(os.path.join(pardir, "static/checkcode/checkwords.json"), "wb"))


def buildcheckcodeimage(inputstr, ri):
    try:
        image = Image.open(os.path.join(pardir, "static/checkcode/checkcode_background.jpg"))
        imagenumber = Image.new("RGBA", (50,50), (255,255,255))
        draw = ImageDraw.Draw(image)
        drawn = ImageDraw.Draw(imagenumber)

        font = ImageFont.truetype(fontpath, 60)
        fontn = ImageFont.truetype(fontpath, 40)
        drawn.text((0, 0), '%s'%(ri+1), (183,50,44), font=fontn)
        draw.text((10, 0), inputstr, (17, 13, 157), font=font)
        img_resized = image.resize((188, 45), Image.ANTIALIAS)
        img_resizedn = imagenumber.resize((20, 25), Image.ANTIALIAS)

        img_resized.save(os.path.join(pardir, "static/checkcode/checkcode.png"))
        img_resizedn.save(os.path.join(pardir, "static/checkcode/checkcode_number.png"))

        ujson.dump({'word':inputstr, 'number':ri}, open(os.path.join(pardir, "static/checkcode/checkcode.json"), "wb"))
    except Exception as e:
        print e
        print os.path.join(pardir, "static/checkcode/checkcode_background.jpg")
        print traceback.print_exc()
        return False


@bottle.route("/sports/login")
def sportslogin():
    return template('sports_login')


@bottle.route("/sports/register")
def sportsregister():
    checkcode = createcheckcode()
    if checkcode is None or len(checkcode) == 0:
        return abort(500, "check code created failed!!")
    print "check number and check code is:", checkcode[0], checkcode[1]
    return template('sports_register', checknumber=checkcode[0], checkword=checkcode[1])


@bottle.route("/checkingcodepage")
def checkingcodepage():
    """
    """
    return template('checkingcodepage')

from bottle import response


@bottle.route("/sports/forgetpwd", method="GET")
def sportsforgetpwd():
    user = request.GET.get('user')
    if user is None:
        return abort(404)
    return template('sports_forgetpwd', user=user)


@bottle.route("/checklogininfoconfirm", method="POST")
def checklogininfoconfirm():
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    ret = {'status': -1}
    if username is None or password is None:
        return ret
    f = RPDB.checkuserinvalid(username.strip(), password)
    if f < 0:
        ret['status'] = -2
        ret['flag'] = f
    else:

        #ottle.request.environ
        try:
            s = request.environ.get('beaker.session')
            s['username'] = username
            s['password'] = password
        except Cookie.CookieError as e:
            ret['status'] = -3
            return abort(500, "your cookie header has been broken, please clear your cookie, and try again!!")
            # print traceback.print_exc()
            # header = request.environ.get("HTTP_COOKIE").split(";")
            # if request.environ.has_key('beaker.session'):
            #     cookies, check_header = request.environ.get('beaker.session')
            #     if check_header == header:
            #         pass
            # cookies = Cookie.SimpleCookie()
            # cookies.load(header)
            # request.environ["beaker.session"] = (cookies, header)
            # # bottle.request.environ['beaker.session'].delete()
            # s = request.environ.get('beaker.session')
            # s['username'] = username
            # s['password'] = password
        finally:
            print "===session save!!!==="
            s.save()
        ret['status'] = 0
    return ret


@bottle.route("/checkregisterinfoconfirm", method="POST")
def checkregisterinfoconfirm():
    """
    """
    code = request.POST.get('code')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    checkcode = request.POST.get('checkcode')
    numbercode = request.POST.get('numbercode')

    ret = {'status': -1}
    if code is None or user is None or pwd is None or checkcode is None or numbercode is None:
        return ret

    # check checkcode
    if verifycheckcode(code, checkcode, numbercode) is False:
        ret['status'] = -4
        ck = createcheckcode()
        if ck is None:
            ret['status'] = -5
        ret['ck'] = ck
    else:
        flag = RPDB.adduser2db(user.strip(), pwd)
        qrcard = createuserqrcodecard(md5value(user.strip()))

        print "------qrcode---->", qrcard
        if type(qrcard) == int:
            ret['status'] = -10
            return ret
        if flag < 0:
            ret['status'] = -11
            ret['flag'] = flag
            ck = createcheckcode()
            if ck is None:
                ret['status'] = -5
            ret['ck'] = ck
        else:
            ret['status'] = 0

    return ret


@bottle.route("/checkuserphonenumber", method="POST")
def checkuserphonenumber():
    """
    """
    user = request.POST.get('user')
    if user is None:
        return "-1"
    # sigin api check it!
    return "0"


def main():
    """
    """
    createcheckcodeimglist()
    print "== done!! =="

if __name__ == '__main__':
    main()
