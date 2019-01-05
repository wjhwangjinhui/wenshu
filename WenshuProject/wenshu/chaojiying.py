#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '96001')
    im = open('a.jpg', 'rb').read()
    print(chaojiying.PostPic(im, 1902))

    """
    英文数字
验证码类型	验证码描述	官方单价(题分)
1902	常见4位英文数字	10
1101	1位英文数字	10
1004	1~4位英文数字	10
1005	1~5位英文数字	12
1006	1~6位英文数字	15
1007	1~7位英文数字	17.5
1008	1~8位英文数字	20
1009	1~9位英文数字	22.5
1010	1~10位英文数字	25
1012	1~12位英文数字	30
1020	1~20位英文数字	50
中文汉字
验证码类型	验证码描述	官方单价(题分)
2001	1位纯汉字	10
2002	1~2位纯汉字	20
2003	1~3位纯汉字	30
2004	1~4位纯汉字	40
2005	1~5位纯汉字	50
2006	1~6位纯汉字	60
2007	1~7位纯汉字	70
纯英文
验证码类型	验证码描述	官方单价(题分)
3004	1~4位纯英文	10
3005	1~5位纯英文	12
3006	1~6位纯英文	15
3007	1~7位纯英文	17.5
3008	1~8位纯英文	20
3012	1~12位纯英文	30
纯数字
验证码类型	验证码描述	官方单价(题分)
4004	1~4位纯数字	10
4005	1~5位纯数字	12
4006	1~6位纯数字	15
4007	1~7位纯数字	17.5
4008	1~8位纯数字	20
4111	11位纯数字	25
任意特殊字符
验证码类型	验证码描述	官方单价(题分)
5000	不定长汉字英文数字	2.5每英文，10每汉字 
(基础10)
5108	8位英文数字(包含字符)	22
5201	拼音首字母，计算题，成语混合	首字母20，计算20，成语40
5211	集装箱号 4位字母7位数字	30
坐标选择计算等其他类型
验证码类型	验证码描述	官方单价(题分)
6001	计算题	15
6003	复杂计算题	25
6002	选择题四选一(ABCD或1234)	15
6004	问答题，智能回答题	15
9101	坐标选一,返回格式:x,y	15
9102	点击两个相同的字,返回:x1,y1|x2,y2	22
9202	点击两个相同的动物或物品,返回:x1,y1|x2,y2	40
9103	坐标多选,返回3个坐标,如:x1,y1|x2,y2|x3,y3	20
9004	坐标多选,返回1~4个坐标,如:x1,y1|x2,y2|x3,y3	25
9104	坐标选四,返回格式:x1,y1|x2,y2|x3,y3|x4,y4	30
9201	坐标多选,返回1~5个坐标值	50
    """
