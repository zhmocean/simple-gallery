# -*- coding: utf-8 -*-
# !/usr/bin/env python

import pymysql
import phpserialize
import config
import os

class WordpressNggDb:
    def __init__(self):
        self.basepath = config.wpconf["base_path"]

    def findMenus(self):
        menus = {}
        gids = set()

        aids = config.wpconf["albums_ids"]
        albums = self.touchDb("SELECT id, name, slug, sortorder FROM wp_ngg_album where id in ("+",".join(map(str,aids))+")")

        for a in albums:
            ags = phpserialize.loads(a["sortorder"])
            gids = gids.union(set(ags.values()))
            a["agids"] = ags.values()
            del a["sortorder"]
            menus[str(a["id"])] = a

        gallerys = {}

        for g in self.touchDb("SELECT gid, name, slug, title, galdesc FROM wp_ngg_gallery where gid in ("+",".join(map(str, gids))+")"):
            gallerys[str(g["gid"])] = g

        for k in menus:
            ma = menus[k]
            ma["gallerys"] = [gallerys[gid] for gid in ma["agids"]]

        return menus

    def findPicturesByGid(self, gid):
        return self.findPictures("SELECT pid, image_slug, filename, description, alttext,meta_data, g.path as gpath, g.name as gname, g.slug as gslug FROM wp_ngg_pictures,wp_ngg_gallery g  where g.gid=galleryid and galleryid ="+gid)

    def findPictures(self, sql):
        pics = self.touchDb(sql)

        for a in pics:
            try:
                a["meta"] = phpserialize.loads(a["meta_data"].encode('utf-8'),decode_strings=True)
                del a["meta_data"]
            except:
                print "META DATA ERROR:", a["meta_data"]
            a["src"] = os.path.join(self.basepath, a["gpath"], a["filename"])

        return pics


    def findRecentPictures(self, count):
        return []

    def touchDb(self, sql):
        ret = []

        conn = pymysql.connect(
            host=config.wpconf["db_host"],
            port=config.wpconf["db_port"],
            user=config.wpconf["db_user"],
            password=config.wpconf["db_password"],
            db=config.wpconf["db_dbname"],
            charset="utf8"
        )

        cur = conn.cursor(pymysql.cursors.DictCursor)

        try:
            cur.execute(sql)

            for r in cur:
                ret.append(r)

        finally:
            cur.close()
            conn.close()

        return ret


db=WordpressNggDb()