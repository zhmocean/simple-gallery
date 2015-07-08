# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
from beaker.middleware import SessionMiddleware

SSO_SESSION_KEY = "SSO_USER"

try:
    import simplejson as json
except ImportError as ex:
    import json

import bottle
import random

# BASE package directory
BASE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Third party static web libraries
STATIC_PATH = os.path.join(BASE_DIR_PATH, 'static')

def generateMenus():
    import wordpress_data
    return wordpress_data.db.findMenus()

def getPictures(gid):
    import wordpress_data
    return wordpress_data.db.findPicturesByGid(gid)

def getRecentPictures(count):
    import wordpress_data
    return wordpress_data.db.findRecentPictures(count=count)

def needSerial(gid):
    import config
    return config.wpconf.get("serial_gallery") and gid in config.wpconf.get("serial_gallery")

def loadWebUI(app):
    @app.route(['/g/<gid>'])
    @bottle.view('gallery')
    def gallery(gid=None):
        galleryid = 0;

        try:
            import string
            galleryid = string.atoi(gid)
        except:
            print "ERROR gid: ", gid
            return bottle.HTTPError(404, "No this Gallery")

        menus = generateMenus()
        pics = getPictures(str(galleryid))
        if not needSerial(galleryid):
            random.shuffle(pics)
        return dict(
            menus=json.dumps(menus),
            pics=json.dumps(pics)
                    )

    @app.route(['/'])
    @bottle.view('gallery')
    def galleryIndex():
        menus = generateMenus()
        pics = getRecentPictures(20)
        random.shuffle(pics)
        return dict(
            menus=json.dumps(menus),
            pics=json.dumps(pics)
                    )

    @app.route('/static/<filepath:path>')
    def static(filepath):
        return bottle.static_file(filepath, root=STATIC_PATH)


def loadErrors(app):
    @app.error(400)
    def error400(ex):
        bottle.response.set_header('content-type', 'application/json')
        return json.dumps(dict(error=ex.body))

    @app.error(401)
    def error401(ex):
        bottle.response.set_header('content-type', 'application/json')
        return json.dumps(dict(error=ex.body))

    @app.error(404)
    def error404(ex):
        """ Use json 404 if request accepts json otherwise use html"""
        if 'application/json' not in bottle.request.get_header('Accept', ""):
            bottle.response.set_header('content-type', 'text/html')
            return bottle.tonat(bottle.template(bottle.ERROR_PAGE_TEMPLATE, e=ex))

        bottle.response.set_header('content-type', 'application/json')
        return json.dumps(dict(error=ex.body))

    @app.error(405)
    def error405(ex):
        bottle.response.set_header('content-type', 'application/json')
        return json.dumps(dict(error=ex.body))

    @app.error(409)
    def error409(ex):
        bottle.response.set_header('content-type', 'application/json')
        return json.dumps(dict(error=ex.body))

def startServer():
    import bottle

    app = bottle.default_app()  # create bottle app

    loadErrors(app)
    loadWebUI(app)

    app = bottle.app()

    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 9000,
        'session.data_dir': 'data',
        'session.auto': True
    }

    app = SessionMiddleware(app, session_opts)

    bottle.run(app=app,
               server='paste',
               host="0.0.0.0",
               port=8030,
               debug=True,
               interval=1,
               quiet=False)

if __name__ == "__main__":
    startServer()
