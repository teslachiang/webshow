# ========= coding:utf8 ===========
import os
from PIL import Image
import traceback
import qrcode
from datetime import datetime
from publicdefine import md5value


filepath = os.path.abspath(os.path.realpath(__file__))
curdir = os.path.dirname(filepath)


def changeimageresolution(im):
    w, h = im.size
    flag = False
    if w > 1000 or h > 1000:
        w = int(w*0.5)
        h = int(h*0.5)
        flag = True
    if flag:
        im = im.resize((w, h))
    return im


def processimage(imgpath, imgfilename, md5id):
    tmpimagepath = os.path.join(imgpath, imgfilename)
    im = Image.open(tmpimagepath)
    im = changeimageresolution(im)
    #headcut_name = md5id + "_headcut" + imgfilename[flag:]
    #headcut = os.path.join(imgpath, headcut_name)
    region.save(tmpimagepath)
    # os.remove(tmpimagepath)


def savearticleimage(username, imagebase64):
    """
    """
    try:
        _imgbase = imagebase64.split(",")
        _imgtype = _imgbase[0].split(";")[0]
        imgtype = _imgtype[_imgtype.rfind("/")+1:]
        imageupload = os.path.join(pardir, "static/userarticleimage/")

        md5name = md5value(username)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        destimgname = "art_%s_%s.png"%(md5name, timestamp)
        _tmpimage = os.path.join(imageupload, "testblob_%s_%s.%s"%(md5name, imgtype, timestamp))
        with open(_tmpimage, "wb") as fh:
            fh.write(_imgbase[1].decode('base64'))

        im = Image.open(_tmpimage)
        im = changeimageresolution(im)
        im.save(os.path.join(imageupload, destimgname))
        os.remove(_tmpimage)
    except Exception as e:
        print e
        return -1
    return destimgname


def processimgcrop(imgpath, imgfilename, cropdata, md5id):
    try:
        if cropdata is None or type(cropdata) != dict:
            return -2
        tmpimagepath = os.path.join(imgpath, imgfilename)
        im = Image.open(tmpimagepath)
        x = float(cropdata['x'])
        y = float(cropdata['y'])
        h = float(cropdata['height'])
        w = float(cropdata['width'])
        rotate = int(cropdata['rotate'])

        box = (int(x), int(y), int(x+h), int(y+w))

        imout = im.rotate(rotate)
        region = imout.crop(box)
        flag = imgfilename.rfind(".")
        headcut_name = md5id + "_headcut" + imgfilename[flag:]
        headcut = os.path.join(imgpath, headcut_name)
        region.save(headcut)
        os.remove(tmpimagepath)
        return headcut
    except Exception as e:
        print e
        print traceback.print_exc()
        return -1


def createuserqrcodecard(md5id):
    try:
        qrcodelink = "static/qrcode/%s_qrcode.png"%md5id
        qrpath = os.path.join(curdir, qrcodelink)
        if os.path.exists(qrpath):
            os.remove(qrpath)
        qr = qrcode.QRCode(
              version=2,
              error_correction = qrcode.constants.ERROR_CORRECT_H,
              box_size=10,
              border=4)
        link = "http://tonghecar.com:9011/sports/user?md5id=%s&qrcodedate=%s"%(md5id, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image()
        img = img.convert("RGB")
        img.save(qrpath)
        return qrcodelink
    except Exception as e:
        return -1


def __createuserqrcodecard(username):
    qrpath = os.path.join(curdir, "%s.png"%username)
    if os.path.exists(qrpath):
        os.remove(qrpath)
    qr = qrcode.QRCode(
           version=2,
           error_correction = qrcode.constants.ERROR_CORRECT_H,
           box_size=10,
           border=4)
    link = "http://tonghecar.com:9011/sports/user?md5id=%s&qrcode=%s"%("dfdfdfdfdfd", datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGB")

    icon = Image.open(os.path.join(curdir, "static/caoren.jpg"))
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h

    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w)/2)
    h = int((img_h - icon_h)/2)

    img.paste(icon, (w, h))
    img.show()
    img.save(qrpath)


def main():
    """
    """
    createuserqrcodecard('sobobtest')
    return
    im = Image.open(os.path.join(curdir, "static/centrum_logo_favor.png"))
    print im.format , im.size, im.mode
    im.show()
    x = 60; y = 89; h = 273; w = 214
    box = (x, y, x+h, y+w)
    reg = im.crop(box)
    reg.show()

if __name__ == '__main__':
    main()
