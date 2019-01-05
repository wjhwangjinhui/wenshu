#!/usr/bin/env python
# encoding: utf-8

import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import os
import platform
import urllib.request
from util import log
from lxml import etree


class ParseHtml(object):
    def __init__(self, html):
        self.html = html
        self.tree = etree.HTML(html)

    def get_tags(self, path1, path3=None):
        """
        获取标签列表
        :param path: 标签路径
        :return: list
        """

        tags = self.tree.xpath(path1)
        if tags == [] and path3:
            tags = self.tree.xpath(path3)
        if tags:
            return tags
        else:
            raise ValueError("path1 没有获取到标签")

    def get_texts(self, path1, path2, path3=None, cols=None, one=False):

        """

        获取标签路径下指定的文本信息
        :param tags: 标签为lists
        :param cols:list为字段对应的key列表
        :param path: 路径
        :return: 文本为一个list,包含item
        """
        results = []
        tags = self.get_tags(path1, path3)
        if isinstance(cols, list):
            for tag in tags[1:]:
                item = []
                ttags = tag.xpath(path2)
                for tag in ttags:
                    text = self.find_text_in_tag(tag)
                    item.append(text)
                results.append(item)
            return results

        elif isinstance(cols, dict):
            for tag in tags:
                item = {}
                texts = tag.xpath(path2)
                if len(texts) == 11:
                    texts.pop(3)
                if isinstance(texts, list):
                    for k, v in cols.items():
                        item[k] = texts[v]
                results.append(item)
            return results
        elif one:
            item = {}
            for tag in tags:
                td_tags = tag.xpath(path2)
                k = self.find_text_in_tag(td_tags[0])
                v = self.find_text_in_tag(td_tags[1])
                item[k] = v
            return item

        else:
            clos = []
            for i in range(len(tags)):
                texts = tags[i].xpath(path2)
                if len(texts) >= 4:
                    slicenum = 1
                    break
            print(slicenum)
            ttags = tags[slicenum].xpath(path2)
            for tag in ttags:
                text = self.find_text_in_tag(tag)
                if text:
                    clos.append(text)
            print(clos)
            for tag in tags[slicenum + 1:]:
                item = {}
                ttags = tag.xpath(path2)
                for i in range(len(ttags)):
                    text = self.find_text_in_tag(ttags[i])
                    if text:
                        item[clos[i]] = text
                if item:
                    results.append(item)
            return results

    def get_one_texts(self, path, col=None):
        texts = self.tree.xpath(path)
        if texts:
            return texts

    def find_text_in_tag(self, tag):
        """
        在具体一个标签里找文本数据
        :param tag:有文本数据的标签
        :return://*[@id="info_id"]/table/tbody/tr[2]/td[1]/p/font/font/span[1]
        """
        textlist = []
        textpaths = ['p/text()', 'p/span/text()', 'text()', 'font/text()', 'p/font/text()', 'p/wenshu/font/text()',
                     'strong/text()']
        for path in textpaths:
            texts = tag.xpath(path)
            if texts:
                for text in texts:
                    text = text.strip()
                    if text:
                        textlist.append(text)
        text = ','.join(textlist)
        if text.startswith(","):
            text = text[1:]
        text = text.replace("：", "")
        return text

    def get_titles_hrefs(self, path2, path1=None, tags=None, host=''):
        result = []
        if not tags:
            tags = self.get_tags(path1)
        else:
            pass
        if not tags:
            return
        for tag in tags:
            atags = tag.xpath(path2)
            if atags:
                for atag in atags:
                    item = {}
                    title = atag.xpath("@title")
                    if title:
                        item['title'] = title[0]
                    elif atag.xpath("text()"):
                        title = atag.xpath("text()")[0]
                        item['title'] = title.strip()
                    else:
                        pass
                    url = atag.xpath("@href")
                    if url:
                        url = url[0]
                        if "http" in url:
                            item['url'] = url
                        if host and "http" not in url:
                            item['url'] = host + url
                        else:
                            item['url'] = url
                    result.append(item)
            else:
                pass
        return result

    def get_url_by_small(self, path1s, path2s):
        ptags = []
        result = []
        for path1 in path1s:
            tags = self.get_tags(path1)
            if tags:
                ptags.extend(tags)
        if ptags:
            for tag in ptags:
                for path in path2s:
                    urls = tag.xpath(path)
                    result.extend(urls)
        return result

    def get_texts_by_small_one_to_many(self, path1, path2, trtags=None):
        results = []
        clos = []
        if not trtags:
            tr_tags = self.get_tags(path1)
            if tr_tags:
                if len(tr_tags) == 1:
                    return
        if tr_tags:
            rstarnum = 1
            log.crawler.info("tr tags length is:%d" % len(tr_tags))
            for i in range(len(tr_tags)):
                dv = []
                dtags = tr_tags[i].xpath(path2)
                for j in range(len(dtags)):
                    text = self.find_text_in_tag(dtags[j])
                    dv.append(text)
                if '纳税人名称' in dv or "案件名称" in dv or "姓名" in dv or '纳税人识别号' in dv or '行政相对人名称' in dv:
                    clos = dv
                    rstarnum = i
                    break
            for i in range(rstarnum + 1, len(tr_tags)):
                dv = []
                item = {}
                dtags = tr_tags[i].xpath(path2)
                for j in range(len(dtags)):
                    text = self.find_text_in_tag(dtags[j])
                    dv.append(text)
                if len(clos) == len(dv):
                    for f in range(len(clos)):
                        item[clos[f]] = dv[f]
                else:
                    pass

                if item:
                    results.append(item)
        return results

    def get_texts_by_small_one_to_one(self, path1, path2, trtags=None):
        item = {}
        if not trtags:
            tr_tags = self.get_tags(path1)
            if not tr_tags:
                return None
            elif len(tr_tags) == 1:
                return None

        else:
            tr_tags = trtags
        if tr_tags:
            rstarnum = 1
            for i in range(len(tr_tags)):
                dv = []
                dtags = tr_tags[i].xpath(path2)
                if len(dtags) == 2:
                    text1 = self.find_text_in_tag(dtags[0])
                    text2 = self.find_text_in_tag(dtags[1])
                    if text1 and text2:
                        item[text1.strip()] = text2.strip()

                elif len(dtags) == 1:
                    text = self.find_text_in_tag(dtags[0])
                    print(text)
                    # text3=self.find_text_in_tag(dtags[0])
                    # print(text3)
                    # texts=text3.split(':')
                    # item[texts[0]]=texts[1]
            return item
        else:
            raise ValueError

    def get_texts_by_path(self, path):
        texts = self.tree.xpath(path)
        if texts:
            result = [text.replace("：", "") for text in texts]
            return result

    def get_urls(self, parent_path, child_path, host=''):
        tags = self.get_tags(parent_path)
        if tags:
            print("first tags length is:%d" % len(tags))
            urls = self.get_titles_hrefs(path2=child_path, tags=tags, host=host)
            return urls
        else:
            print("第一步的tags没有成功获取......")

    def down_excel(self, url, fold, ffx='.xls'):
        """

        下载文件
        :param item: 包含title,url
        :param fold: 文件夹名称
        :param ffx:文件后缀
        :return:
        """

        print("开始下载excel文件")
        pl = self.getsystem()
        if pl == "Linux":
            filedir = "/home/biuser/data/tax/{fold}".format(fold=fold)
        else:
            filedir = "D:\\data\\tax\\{fold}".format(fold=fold)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),
                             ('Host', 'www.jx-n-tax.gov.cn')]
        ffx = os.path.splitext(url)[1]
        excelfile = os.path.split(url)[1]
        if "=" in excelfile:
            excelfile = excelfile.split("=")[-1]
        else:
            excelfile = excelfile

        try:
            if pl == "Windows":
                excelfile = filedir + "\\" + excelfile
            else:
                excelfile = os.path.join(filedir, excelfile)
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, excelfile)
            sizenum = self.get_FileSize(excelfile)
            print("excel 文件下载完成 size num is:%s,excel name is:%s" % (sizenum, excelfile))
            return excelfile

        except Exception as e:
            raise e

    def get_FileSize(self, filePath):
        fsize = os.path.getsize(filePath)
        return fsize

    def getsystem(self):
        pl = platform.system()
        return pl
