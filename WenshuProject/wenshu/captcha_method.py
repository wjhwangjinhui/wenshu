# -*- coding: utf-8 -*-
import os
import re
from PIL import Image, ImageDraw, ImageFont
from wenshu.chaojiying import Chaojiying_Client


def compose_pic(tip, img_path, compose_img_path):
    """ :param tip: 是要合成的文字，# 举例：tip = '请依次点击图中的"逢 泼 诋"'
        :param img_path: 网站原始验证码图片下载后的路径
        :param compose_img_path: 合成后的图片路径
        :return:
    """
    im = Image.open(img_path)
    width, height = im.size
    # 新建一个白底图片
    black_img = Image.new('RGB', (int(width), int(height / 2)), (225, 225, 225))
    text_img = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'text_img.png')
    black_img.save(text_img)
    # 给图片加文字
    draw = ImageDraw.Draw(black_img)
    new_font = ImageFont.truetype('simkai.ttf', 16)
    draw.text((int(width / 12), int(height / 8)), tip, (0, 0, 0), font=new_font)
    # black_img.show()
    black_img.save(text_img)
    # 把text_img 和 im这两个图片上下拼接
    target = Image.new('RGB', (int(width), int(height * 1.5)), (225, 225, 225))
    target.paste(im, (0, 0))
    text_img = Image.open(text_img)
    target.paste(text_img, (0, int(height), int(width), int(height * 1.5)))
    target.save(compose_img_path)


class Recognize(object):
    def __init__(self):
        self.resp = Chaojiying_Client('', '', '')

    # 调用超级鹰识别验证码
    def recognize_captcha(self, file_name, captcha_type):
        """ :param file_name: 验证码图片的路径
            :param captcha_type: 验证码的类型,举例：1902	常见4位英文数字，2004	1~4位纯汉字，9103	坐标多选,返回3个坐标
            :return:
        """
        # resp = Chaojiying_Client('zhangqm', 'Za88123456', '96001')
        im = open(file_name, 'rb').read()
        result_dict = self.resp.PostPic(im, captcha_type)
        # print('result_dict',result_dict)
        result = result_dict.get('pic_str')
        pic_id = result_dict.get('pic_id')
        """常见4位英文数字
            {'err_no': 0, 'err_str': 'OK', 'pic_id': '6040109541662100016', 'pic_str': '88g6','md5': 'c2afee222913851665b8d2d68254337f'}"""
        """坐标多选,返回3个坐标
            {'err_no': 0, 'err_str': 'OK', 'pic_id': '6041014421662100001', 'pic_str': '22,23|67,98|169,49', 'md5': 'd6eaa6ccf65c04b3ec0ee754573b1f2d'}
            22,23|67,98|169,49"""
        print(result)
        if captcha_type == 9103 or captcha_type == 9102 or captcha_type == 9004 or captcha_type == 9201:
            r_li = re.findall(r'(\d+)\,(\d+)', result)
            print(r_li)
            if r_li:
                li = [{'x': r_li[i][0], 'y': r_li[i][1]} for i in range(len(r_li))]
                print(li)
                return li, pic_id
        else:
            return result, pic_id

    # 如果验证码错误，返回图片的id，有报错返分
    def report_err(self, pic_id):
        self.resp.ReportError(pic_id)
        print('报错，申请返分')

