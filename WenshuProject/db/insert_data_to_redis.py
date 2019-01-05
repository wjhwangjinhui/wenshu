#!/usr/bin/env python
# -*- coding: utf-8 -*-


import platform
import redis

pl = platform.system()

if pl == "Linux":
    redis_obj = redis.Redis(host='127.0.0.1', port=6379, db=1)
else:
    redis_obj = redis.Redis(host='master', port=6379, db=1)


def start(file):
    file = open(file, "r", encoding="utf-8")
    content = file.read()
    lines = content.split("\n")
    words = list(set(lines))
    print(len(words))
    wfile = "shixin_court_words"
    redis_obj.sadd(wfile, *words)


if __name__ == '__main__':
    file = "court_shixin_words.txt"
    start(file)
