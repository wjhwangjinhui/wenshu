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
    # run_eval = "w61aw51uwoIwFH4WwowXbVjDtgLDhCsfYcKXJw1Zw5ApF8OKUsOZwpXDscOdB0gQKSjCjMK2dMO4JcOkEMOaw7PDt309bcOawobDpT7DnmxPwpHCjMK/w5PDlUcqw6PDo8Ouw71LJsKHw7XDvlPCrsKTw43ClsO5wp5PAsOCacOxBhIgXsKjQsOmAMOkRcKmK1YlwowtBHgHwrMQGD0wwobDgQUJwoAOJkAHw7DCgx3CoAYxw6AEPAEcAAMSRgACwoXDoMKgw6BBEMKuFlFyPMKlw7InShPCuQhCCkXDtjDDpsKfL8K5WsO1wpwvwpzCrsKWwpQJIXzDphUdwpzDrn3Dph3Dj3vCisOPw6XDrcOvBGJ5c8KmQV7DnkPCgsKyVyPDoMK9wrpXGnQHa8Okw53CqsO7MMKnwrrCt8O2w7YqVMKRwrVKwpHCkkIrwoYHwr7CqyTDuzFaw7t8wpp2T8KNIWrCg3XDv2Yww4JqwqzCqRZ7fU7DlFI3w6B/w4DCtDYFw5HCrE/Cs8KOLXjDl1nClcKsw4dyOEvDqB10dCzDrWbCi8OFw6bCjMOSX0ETUGbCq8OSZhnDp8K/wpTDlnzDmcKyNGl0w645HMOYQsOpwotoPx3Cq2EnwoLCh8OYE8OFdiPCgTILw5Y4wpLDtjpwO8OJV8OLw7laAUfDpX0Jw53Dri/ClMOWwrpDGnFDw6AQecOIw6cawpEzHsO8Ag=="
    # docid = "DcKOwrsNADEIw4VWw6JBw7jClQTDgsO+I8OdVcKWXFjCphNow6rCucOnwq7CscK0FsO0NMKlw5s7worCgcOxwqZaC8KlwrFHw4Nww41bKWrDg8KLfEfCssKqw5nCksK1wrfCpBg6P8Kpw7zDkkzChcKLIsOCwq3CghjDsjIUwp7DmTMPw5EBw6RswpbDosOPwr/Cu0XCizk3wpTDqxVfw7A5w7LCggZuwppFw5QdIyvDv2jDrcKjKWxaFcOKHcK/woHDsMKjwrYXL20zSsOFw7UD"
    # run_eval = "w61bQW7CgzAQfAtRDkZUw70Aw4opT8OoccKFwqLCiMKkDcKHwobCisOQU8KUwr8XKCXCgMOBQDFgwpvCkcOQRMKAwr07wrs7CzZSwrbCl8OgdMK+w7lRw7AVw6/DnsOiKMK4fsK8wr5Hw6HDp8O+csKMw7bDocOpw4wcw4shD8KgNMK8IAnCgHUow4TChEBWw5LCrngqwqHCtgDDpB3CmQXCoHrDiBjCisKLfCIxCBjCgAoAwqALFA5JACDCqSgXAABNwqHChAgdACEgVsOAw5oBwqpBwp5MDMOOwqzCkMOQwqUAw4gJUQPCoDPDhAVYCcOYwq57w5htw7zDsHrCi8Kjbz8OwqPCjXvCoMKDwpccwow5w7dHOsKsOMOuD8KbfmdSAsKew6cwK8K7YVPDlWZ6wqPDu052wrp9w75jwoVYejkZQVZ6woc8Sn5qDsKrw4PCrXxCwrvCsxrDr8OGwrFCTmVrw43DlwtXGWs+RRzChcOGGATCtgvCksO9Mlo6w63CpMOdc8OEwpBhwoPDh8O+b8OCwohZY8KnSsKZL8OPSFUefMKnZgfCqzXCvTzDjzLCs1HDqhXCkcK+wofDiXvCocKKTGtzWsODM1jCn8OLw4XCrH4GO8KbwpXDmEIewpd0wqvCmMOvfMKBw5PCssKIwqHDjiXCiMOBwolSwoPCgDwWw60LQhVCw7zCo8OYwr7CpCTDmcOvWCUWXHPCqUQ1wrLCkknCqcK9w6jDkmBJwqhaQcOLNsOrwr3Dn2tzwqxQw4wNO2AuJMOKw7dFw7TDvMOCw4BdLRvCpBF7eHXDtQN6wqPDusKjXXYCQRrDtcONS2nDpcOUw4vDhcOHwp1fw6jDv8KVc2zDmMKGwr/CmVbCs8Kbwq3DqEvDkMK5w7zCo0LDlMK4WsK+PsK0IcKqTR4Lwp3DkHTCnznCkXAtKGvCmMOCbsOewobDr8KNw7UiwqrDukPDm2bCtsO7Aw=="
    run_eval = "w61aw4vCjsKCMBTDvRbCjMKLNkzDpgfCiCs/YcKWNw0xwogjwosRU8KZFcOxw58HEBkeVVAKVjgJwrnChsO2PsOOOcK9LcKQwrjDnAdbw7/DpMOJw6AYwq3CviIZHMK+P3cyw7xZw683ch1ufWZbNgkYwqPDjQdEwoDCmUfCh0zCgcOITMK2K04lwqwtDHTCh8KyMFg9KMKGw4XChQggDDnDgBrDlMOBH8OqQAloAmHCoBPDiMKBElYABsKNYMKgw6HCjsOjwq4WXng4RcOyw5fCi0LCuXBcckVyMWbDh8Onw5TCrcK4w6IzwqdLJCVGCMKbWcOZBMKnasOOdMKifSbCu13DvsO/O8KBWDrCnHjCkMKVw47CkMKgw6TCp1bCsMOqbsOlAcK3wovDlXArfcOvYipnU8KPF8KlMsOUTcKJGhDClBzDrsOkLkB2U8K0dMObCsK7wqPDhyNuD8O7PhfDkCPCqm/CqMKWeH1JwprCrcKuahrDjcO1w5rCt8K5GsKOclQrwqhhwogOAcOxw5bCiWFYY8Opwqc+bMOiEcKywo9VYsOUOsOXwq7DlH9iDMK0fcOaw47CnsOrC8OEw4TCmmLCvMK+wpvCq8OCLxPDnMKAVxLDjWVfwoTDqcOtO2XDmsKZw54VQMKOwqLDvsKIw6zDtMO5aMKkXsKKwq/DhQY5wqocw7XDqsORckLDqsOxwr1rwpB4w4BTKsOLGXfDvgA="
    # docid = "DcKOw4ERAEEEBFNywpjDhRNLw74hw51+wqfCqsK7w4fCvX3DtxsiwqnCrcKQETbCocKjw4fChB12wpB0wqnCsXxWJMORWcO0wrk+Rk0qO8OyHMOoEygTwpTCp3RYwotOcmAjJcOjbhcaw71pC8Kuwo3Dr2sVw5/Dj8KBw5tCe8OAZsOTGMKWwqzDq8KDwoAPwpcNRTDCrMOkwpvDth48wpXCvcKdNHfDpcKywpdpw49ywqbDn8K2w5UtM8Oawp3Dt1Zew5zCosK/WMO2Hw=="
    docid = "DcKOwrkRADAIw4NWwoLDsMKXQGDDv8KRwpLDhsKNw4/CkgV2S2VRN8O6VBJRcVnDtsKQwo4sB8K7KRvCnGjDisONwqpGwrlgwr0Rwp5Fwq7CmcKIUsO3wq7DqXDCsS7DvcOVQE1WExrDnRbCoCViw7fClcOgK8OKfMKsbRE0woU7w44EYMOMIRjCi8OFI8OzScO3Z8OEbxhaAcKQwocOVsKew6vCjcOYwr47DMKewqNMwqDDv8OIBwbCs34HHsOowoorw65fSVcf"
    id = doc_id(run_eval, docid)
    print(id)

