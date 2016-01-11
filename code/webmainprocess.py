# ========== coding:utf8 ============
from publicdefine import *

app = SessionMiddleware(bottle.app(), session_opts, environ_key='beaker.session')


# ============= static field ===================
@bottle.route("/static/<filename:path>")
def server_staticfile(filename):
    return static_file(filename, root=os.path.join(pardir, "static"))

# ============== public interfaces ==============


@bottle.error(404)
def error404(error):
    """
    """
    return template("404")

# ========= import background module=========
from backgroundmodule import *


# ========= import mainpage module=========
from sports_mainpage import *

# ========= import personalsocial module=========
from personalsocial import *
# ========== import personalmail module================
from personalmail import *

# ========== import personalarticle module================
from personalarticle import *
from circle import *
from addfriends import *
# ========== import personal info==============
from personalinfo import personalinfobasic, uploadshortcut


# ========= import personalsocial module=========
from userregistermodule import sportslogin, checkuserphonenumber,\
                               checkregisterinfoconfirm, sportsforgetpwd, \
                               checkingcodepage, sportsregister, checklogininfoconfirm


def main():
    """
    """
    run(app, host="localhost", port=9011, debug=True, reloader=True)


if __name__ == '__main__':
    main()
else:
    pass
