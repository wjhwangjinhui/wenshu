#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib


def getmd5(hashname):
    hashstr = hashlib.md5(hashname.encode("utf-8")).hexdigest()
    return hashstr
