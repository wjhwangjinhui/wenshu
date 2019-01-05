#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/20 13:53
@Author  : wangjh
@File    : get_docid.py
@desc    : PyCharm
"""
import os
import sys
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))



cur_dir = os.path.dirname(os.path.realpath(__file__))
a2 = os.path.join(cur_dir, "a2.js")
import re
import execjs
b64tab = {'0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61, '+': 62, '/': 63,
          'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
          'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
          'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36,
          'l': 37, 'm': 38, 'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48,
          'x': 49, 'y': 50, 'z': 51}
def fromBase64(str1):
    str1 = str1.replace('-', '+').replace('_', '/')
    str2 = re.sub('[^A-Za-z0-9\+\/]', '', str1)
    return _decode(str2)
def _decode(a):
    return btou(Base64_atob(a))
def Base64_atob(a):
    return re.sub('[\s\S]{1,4}', cb_decode, a)
def fromCharCode(n):
    return chr(n % 256)
def cb_decode(cccc):
    cccc = cccc.group()
    l = len(cccc)
    padlen = l % 4
    n = (b64tab[cccc[0]] << 18 if l > 0 else 0) | (b64tab[cccc[1]] << 12 if l > 1 else 0) | (
        b64tab[cccc[2]] << 6 if l > 2 else 0) | (b64tab[cccc[3]] if l > 3 else 0)
    # print n
    # chars = [
    #     fromCharCode(n >>> 16),
    #     fromCharCode((n >>> 8) & 0xff),
    #     fromCharCode(n & 0xff)]
    chars = [
        fromCharCode(n >> 16),
        fromCharCode((n >> 8) & 0xff),
        fromCharCode(n & 0xff)
    ]
    p = len(chars) - [0, 0, 2, 1][padlen]
    chars = chars[0:p]
    return ''.join(chars)
re_btou = '|'.join(['[\xC0-\xDF][\x80-\xBF]', '[\xE0-\xEF][\x80-\xBF]{2}', '[\xF0-\xF7][\x80-\xBF]{3}'])
def cb_btou(cccc):
    cccc = cccc.group()
    if len(cccc) == 4:
        cp = ((0x07 & ord(cccc[0])) << 18) | ((0x3f & ord(cccc[1])) << 12) | ((0x3f & ord(cccc[2])) << 6) | (
                0x3f & ord(cccc[3])),
        offset = cp - 0x10000
        # print offsetoffset
        # return (fromCharCode((offset >>> 10) + 0xD800) + fromCharCode((offset & 0x3FF) + 0xDC00))
        return fromCharCode((offset >> 10) + 0xD800) + fromCharCode((offset & 0x3FF) + 0xDC00)
    elif len(cccc) == 3:
        return fromCharCode(((0x0f & ord(cccc[0])) << 12) | ((0x3f & ord(cccc[1])) << 6) | (0x3f & ord(cccc[2])))
    else:
        return fromCharCode(((0x1f & ord(cccc[0])) << 6) | (0x3f & ord(cccc[1])))
def btou(b):
    return re.sub(re_btou, cb_btou, b)
def get_js(data):
    with open(a2, 'r',encoding='utf-8') as f:
        js_data = f.read()
    eval_js = execjs.compile(js_data)
    data = eval_js.call('zip_inflate', data)
    return data
def unzip(str1):
    return btou(get_js(fromBase64(str1)))
def getkey(run_eval):
    a = unzip(run_eval)
    str1, str2 = re.findall('\$hidescript=(.*?);.*?\((.*?)\)\(\)', a)[0]
    js_func = str2.replace('$hidescript', str1)
    aes_key = execjs.eval(js_func)
    keys = re.findall('com.str._KEY=\"(.*?)\";', aes_key)[0]
    return keys

def doc_id(run_eval,docid):
    with open(a2, 'r', encoding='utf-8') as fp:
        js = fp.read()
        ect = execjs.compile(js)
        keys = getkey(run_eval)
        str = unzip(docid)
        id = ect.call('com.str.Decrypt', str, keys)
        return id

if __name__ == '__main__':
    run_eval = "w63Cm8ONbsKCQBTChcKfBcOTw4UQwprCvgBxw6UjdHlDTMKjwrbCusKoNEhXw4Z3L1jCggIjwqAgw47DoMKXwpBjwoDDuTnDt8Ocw4PCncKBw4TCl8O1ZsK5w5otwqLDjU88fcKPwqPDjcO2w6vDrTMKwr9nw6vCj2gWLlfDinM8CQDCo8OhFRHCgMOncMOIGAJ5wpLDh8KVwqpEbgF0R1nCgMOswqEYw4lFDsOUQXIAPcOJFMKAYVACQEoAwosBw6TCjFjDkRjCnQgOYQjCmMKQwp4Tw4gAMEIjYGsAOwF4worCqAF8RlwAcBPCuMK+P8KfThbDoXYXR8K/wos4wowmw75cw6ZBcijDpcOtD2nCs8O8w5gfXMO5w68pCQTCgcKnwpzDow1XwopjwqY3wprDrxxPX05/wpcSwpVeTlrCiMKTw57CkUDCksKfw5LChMOFw6ZOw5bDocOyZCXDnsOawrbCtcKcw45Hw5Nfw4/CpzrCssKuSlTCocKgwo3CoWbDrMKcZDtFw49OG2nCt2xxTcKzwqvDm8Oew5bCoUPCr8KuXXvDqcOfw58gPcKPdMKPw6HDrsOvwp/DtiTCrn48DMKSwrAQwodkVVlOVcKyWm10dcKzby7Cg8KEO0jCllpXY8KDAsOSLnJFbwzClMKkRlXDtcKWw61RCMOdw5puaMKFNWjCsgfDjcOYw6jDlcOqwobDp0Ekw6s8bcOALsOibml/ODvCg1jCmEYFPhbDsjHCl1TDhkzClcO2w4bCrV7CjMKtw5FVwrPDucKvBCw1wrtqw50aJR3DnsOuDRcUwo43PDjClx1Xw6PDhVF9CDPDny/DpcKcVcKDw48uwrTDv8O+w5k1dlZOW31kA8Obw7pSwqJ7w4/CulxJw6xdw4osdMKYwoXCssOmBsKSIcK+wrLCkgTDk8OJW8KtXnMEfCMZCWUrwpYDV8K5w74f"
    docid = "DcKMwrcRw4BADMKAVlIOwqVeYcO/wpHDrMKWAyjCvcO9wqHDpijDgBvCjRdRHsKiPsOQZsOLGCI3wojDgXPCt2jDk8OywrNxOnzDs8OCU8OEMB5pw5BSbsOXwqXCpQPDsR/CjMOaBnhGw6bDogXDgS7DuMK5SBIbw5/DmsOdwpPCom7DtsK9M8OEw7J/wo1PwpwARmB5KgoRWCbCucK3wq/CtUfCt8KaPMOaw51cw5Z8EyvCosKNRMO7N8KPT8KSQxvCmyg/"
    id = doc_id(run_eval, docid)
    print(id)

