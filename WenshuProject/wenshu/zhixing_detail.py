#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/15 14:46
@Author  : wangjh
@File    : zhixing_detail.py
@desc    : PyCharm
"""
import os
import random
import sys
import time

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import platform
import socket
import os
import re
from util import log
from wenshu.doc_decrypt import doc_id_decyrpt
from PublicSpider.common import getmd5
from model.handle_redis import HandleRedis
from util.re_req import re_request
from PublicSpider.get_content_static import get_html
from wenshu.get_docid import doc_id
from util.headers import my_headers
hr = HandleRedis(7)
pl = platform.system()


def get_detail_info(**kwargs):
    run_eval = kwargs.get("runeval")
    doc_id_src = kwargs.get("docid")
    result = doc_id_decyrpt(run_eval, doc_id_src)
    # result = doc_id(run_eval, doc_id_src)
    # log.crawler.info("密钥为：%s" % result)
    url_doc = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=' + result
    item = {"data_source": "http://wenshu.court.gov.cn/"}
    item["CASE_NAME"] = kwargs.get("CASE_NAME", "")
    item["CASE_TIME"] = kwargs.get("CASE_TIME", "")
    item["CASE_TYPE"] = kwargs.get("CASE_TYPE", "")
    item["CASE_NUM"] = kwargs.get("CASE_NUM", "")
    item["COURT_NAME"] = kwargs.get("COURT_NAME", "")
    hashstr = item["CASE_NAME"] + item["CASE_TIME"]
    hashvalue = getmd5(hashstr)
    item["hash"] = hashvalue
    if pl == "Windows":
        filedir = "D:\\workplace\\wenshu_zhixing"
    else:
        filedir = "/data/wenshu_zhixing"
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    item["IP"] = myaddr
    file = hashvalue + ".html"
    file_name = os.path.join(filedir, file)
    item["DOC_DIR"] = file_name
    # i = 0
    # while i < 10:
    for _ in range(1000):
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
            'Cookie': None,
            # 'Accept': 'text/javascript, application/javascript, */*',
            # 'User-Agent': random.choice(my_headers),
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'Host': 'wenshu.court.gov.cn',
            # 'Referer': 'http://wenshu.court.gov.cn/content/content?DocID={}&KeyWord='.format(result)
        }
        resp = re_request(url=url_doc, headers=headers)
        resp.encoding = resp.apparent_encoding
        a = resp.text
        # a = get_html(method='get', url=url_doc)
        text1 = re.findall(r'\\"Html\\":\\"(.*?)\\"}";', a)
        if len(text1) > 0:
                t2 = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Title</title>
                </head>
                <body>
                %s
                </body>
                </html>
                """
                a = t2 % text1[0]
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(a)
                log.crawler.info('数据保存成功......')
                table = "TB_WENSHU_ZHIXING"
                hr.cache_dict_redis(table, item)
                return



def main(**kwargs):
    result = get_detail_info(**kwargs)
    return result


if __name__ == '__main__':
    data = [{
        'RunEval': 'w61Zw4vCjsKCMBTDvRbCjMKLNsKYw7kBw6LDik/CmMOlTUMMOiPCixFTcWXDvMO3AcOGYXgUwotDKcKNwpzChFxDex/Dp8KcPmjDo8OyEMOvw7bDp0jDhsKndMO9wp7DisO4w7jDucO2IcKTwq/DjWErN8OJbsOPfMOPJwHDo8K0WUEEwph5w4zCkFcgMsKTw6XCil0JYwsDw53CoSwMRg/CimFww4EaIkAOaALDvlAHSkAYw6gEciAMShgBGEwEdw0PwoJwwr3CiMKSw6M5wpXClyhNw6QiCCkUw5nDg8KYf8K9w6Vuw6Vzwr1xw7rCicKkw4wIw6Ezwq/DqMOgVMOPwpl3w6h7worDl8Olw59fw7TDhMOyw6bDjMKDwrzCvMKHBGU/wo3CgnV3w68ew5BdwqzCgVvDqcO7EFM1wpvCusK9LFXCoG5Lw5TCgsKgw6TDsCB3CcKywp/CosKVVy3DrMKeHsOPwrg9w63Du8K/woABUUNDwo3DhMKbS2I4w5MYw6lGw4zDmcK9w7bCnRdkHMKcwpYEwpnCoMOuw6gMOnZwIwvCvcOyGcKwRMOIXAnDh8O2wropZDU5wos7Two9DiHCrsKxw5Fyw5Udw41+T3nClsKwwrnCncOdw5bCuMOowotZRWJ5TsOaZsKGwrLCtsOKTl7Duw7CgDVuYMK9w67Cl8KuwqnCpMK4ScK2eFFtD1fCt1YTw5LCgMK7wrAbwrrDjRrCisOgwowHw58=',
        'Count': '469638'}, {
        '裁判要旨段原文': '本院认为：1、东方石办将债权转让给相宜公司后发布债权转让公告，可以认定其已依法履行了对债务人的通知义务。河北高院依据相宜公司的申请，裁定变更其为申请执行人，符合《最高人民法院关于金融资产管理公司收购、处置银行不良资产有关问题的补充通知》第三条关于“金融资产管理',
        '案件类型': '5', '裁判日期': '2012-06-28', '案件名称': '石家庄常山纺织集团有限责任公司不服河北省高级人民法院裁定追加其为被执行人申请复议案执行裁定书',
        '文书ID': 'DcOMw4kBRFEEBMOAwpRsD33DhCfDv8KQZirCgMOibcOVwqbCpcOqLMKhw4PCtsOpKcKlOAU/L18zw4zCnMOpeyfDjTpYwr7CnnLCs2zDnjzDo8Ogw6bCkcKGCGQ/wrcXwr0iwqx6w5HCsSXDrMO8MsOmRXDDtn8ewqjDuzsTO8KXE8K9KsO7Sj3DizNyAlp6w6jDgcOgc0LCjMOlwrtgworDqyN1w4zCgi0IPsKFNSQqaiLDgi/Cq8Oww5Quw5kIdMOLPw==',
        '案号': '（2012）执复字第9号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，人民法院对债务人的财产采取查封措施，其目的是为了保障债权人债权的实现，确保实际变价处分时债权能够得以足额受偿。当然，为避免损害债务人的合法权益，《查封规定》第二十一条也对查封财产的价额作出了限制，即以足以清偿法律文书确定的债权额及执行费用为限，不得明',
        '案件类型': '5', '裁判日期': '2015-05-29',
        '案件名称': '云南圣灵房地产开发有限公司、昆明圣灵房地产开发有限公司与天津土钍投资咨询发展有限公司股权转让纠纷、申请承认与执行法院判决、仲裁裁决案件执行裁定书',
        '文书ID': 'DcKNw4kNADEIA1vDog55wrIGw7ovacOzwrFswo00VmvCqMK7w40dw5rDqW1GJcKHYGs/wpELPGbCscKDD8OpYcKlMcKjU8K8w73CjWAmwpY/X2wPccOUwojDpsO2cVcKwp7Do3QwbcKUdGrCicOFG8K3VMKJwrbDslvCkcOZwrfCnV0ZcsKlX3wFwpwMIgjCnMOzbG7CmMKldsKLw4vChsOqw7t4KkfCl8OgUsO2ecKCw6jDg8K4VsKvwrFewpvCoMO4w7h2E8OiBw==',
        '案号': '（2015）执复字第4号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，本案的焦点问题为，八建公司、道隆公司与江北国投公司签订的相关和解协议是否已经履行完毕，分析如下：\n《执行和解协议》中约定，道隆公司承担向八建公司支付共计13875062元的责任，江北国投公司对道隆公司的给付义务提供担保。尔后，三方又共同签订了一份《',
        '案件类型': '5', '裁判日期': '2013-11-21', '案件名称': '重庆建工第八建设有限责任公司申请复议案执行裁定书',
        '文书ID': 'DcOLwrkBA0EIBMKwwpY4fkIYw5jDvkvCssKVK2nCnRlrZyjChsKubkp1wrLCuA1bw5fComPCtsKXw6PCo0pVYMK+w5I4WcKlw7jDqm0AB8OSw6V5w5bCn8K+wqsJw685Tm/DlFjDncOZDcKcK03DgsOvw6rDvsKnCcKlw6DDrsKIADs3w7JGPR/Ct8OLCsOuC2jDilBLwq3Dq8OnF8O0wok9wqXDlsOUQsKIw5/Ck8KNwqDCnWs9wrg3G8KZR8OYwqxJwofCjsONw4sf',
        '案号': '（2013）执复字第4号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为：本案的争议焦点是，一、重庆高院在执行过程中是否变更了生效判决确定的执行顺序，进而能否执行中侨公司持有的涉案股权。二、涉案评估报告是否已经过期，对中侨公司持有的西部信托有限公司股权是否存在评估价格过低的问题。三、重庆高院的执行行为是否违反法律规定侵害中',
        '案件类型': '5', '裁判日期': '2016-06-27',
        '案件名称': '重庆中侨置业有限公司、中国信达资产管理公司重庆市分公司与重庆中侨置业有限公司、重庆康信置业有限公司等信用证纠纷、申请承认与执行法院判决、仲裁裁决案件执行裁定书',
        '文书ID': 'DcKONQHDgEAMAC3ChWHDjAfDvEtqBRzCpMOASgc7wrjCmMOSMy7Dt0tDfhXDj3PCtB/DmCbCiVYOOcOoNSDDiXY4wp7DsE/DjsKuJ8K6w6lpE3tcEjUjasKVOQkJwp9uNFBIBsOTIcOmwoZ4wqPDvMKtYVPCqMKxIXo4w4QsChZXRhFRf38tw59OMWzCjxzCv8O/c8O5F8OQdcOawrsSFcO9wqfDl8OewptowoTCiQrCpcKabsOPc8O5AA==',
        '审判程序': '', '案号': '（2016）最高法执复20号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，本案的焦点问题是，潍坊银行交给潍坊农商行金额共计5000万元的银行转账支票及相应利息并缴纳执行费用后，是否应视为执行完毕，是否仍需继续履行付款义务。&#xA;首先，本案执行依据是（2003）鲁民二初字第26民事判决，该判决判令潍坊银行及其文化路支行向',
        '案件类型': '5', '裁判日期': '2016-08-11', '案件名称': '潍坊农村商业银行股份有限公司与潍坊银行股份有限公司、潍坊银行股份有限公司诸城支行票据追索权纠纷执行裁定书',
        '文书ID': 'FcOOwrcRA0EMw4DDgMKWeMO0DGnDuy9Jwq8cwrMDwofCgkVZCMKGeTbDkUQMbcOzwoLCpSzDtMOKw7nCsEnDpDUmNHd0wqPDgMOwwp7DqlcgwqjDqz7CpsOMw6BNwqLCjhpHPEvDtg/CtsOawrXDnMOUwr48ODTDncOycjnDmh0LwrZTasKNG8OZGcKqUB/CpMO4NMKqw4lmeVfCqMO/JUfCkTHCm0XCosOqwp4FwooIwpfDvGrDtsOCw7FlU2HCpDoowrp0w5XDtwM=',
        '审判程序': '', '案号': '（2016）最高法执复19号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为：本案争议的焦点问题是，嘶马公司于2011年4月21日出具给三峡旅游学院的《承诺书》中放弃的权利应如何认定问题。&#xA;依据法律规定，连带责任的特点在于责任主体之间承担责任无先后之分，权利人可以请求部分或者全部连带责任人承担责任，不论权利人请求何人承',
        '不公开理由': '', '案件类型': '5', '裁判日期': '2017-03-07',
        '案件名称': '扬州市江都区嘶马建筑安装工程有限公司第八工程处、中国工商银行股份有限公司三峡分行建设工程合同纠纷执行审查类执行裁定书',
        '文书ID': 'DcKMw4kNADEIA1vDogjCsDwxwoTDvkvDmjxsw4kzwpJNVy8ywrwlWMKOViTCsFXDqcOJPcKFwrVYb8OVw7bCj2IMXEDCoAhzwrHDj1gQYsKlDQ8Gwp8swovCuTHDsg3Dr8KjG8OpVikTL8O5cRx+wr/DuDxbXsOdW8KYJ1TCmMKUw7oUw63CqMKtXw7CpcOtw4hmw7fCt3PCmC/DnU7DsgPCqcOGBcOtwoExQjLDhcOqO8O3woMfYcKUw6XCnsKWVhJmw74B',
        '审判程序': '', '案号': '（2016）最高法执监408号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，本案的主要争议焦点为：一、本案是否应参照适用《纪要》规定于正中公司受让债权后停止计算利息;二、本案执行依据所确定利息的计算期间;三、复议裁定对本案利息计算中的罚息利率予以调整是否妥当;四、复议程序是否违法。&#xA;一、关于本案是否应参照适用《纪要》',
        '不公开理由': '', '案件类型': '5', '裁判日期': '2017-08-31', '案件名称': '广州正中投资有限公司、广州市泰和房地产开发有限公司执行审查类执行裁定书',
        '文书ID': 'FcKPw4cNADEQAlvDmsOgTU9vw6rCv8Kkw7PDvRAgNMKoQ8OXwp3DknXDmkgdOgXCilvDqMKDeMKfwrNGPR1zw43DrsKTWjQ8wokOwowYUDLCoBTDgcO/wo7CjcKPwpwbwpZ5eBNRfMOiZcKnw44BLgfCuMOiwpYAw5PCjsKhwqtCGMOrWBl4w4bDuALCtMOUwoA5YMKzwrLDtHrDlWzDmsOpwqbDtMOeHRB/AMO5woDDmCLDksKQwqANMsKGGEbDqFU1asKlw5jDrzs0Hw==',
        '审判程序': '', '案号': '（2016）最高法执监420号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，本案的争议焦点为：一、关于1994年10月17日至1999年8月11日期间的利息计算是否正确的问题。二、关于在确定1996年4月20日之后借款利息的计息基数时，以已付利息扣除截止1996年4月20日的应付利息后，多出部分冲抵借款本金是否正确的问题。三',
        '不公开理由': '', '案件类型': '5', '裁判日期': '2017-12-27', '案件名称': '海南宝贝房地产开发有限公司申诉一案执行裁定书',
        '文书ID': 'HcOOwrcRA0EMw4DDgMKWw4jCpw9pw7svSTdKwpFgZyUqwoPDksKDwoDCtsONKcOmwpzClcOowqvDr1jCqEnCnQ9UOnEQw6s2CcKLw4l4wrTCojhCbD9Iw4zCqsOXw7HCszTDsDplw4vCiMO1MHXDuVrDisOVFMK+wpMTUcOIw5TDocOmwrfDqxFBw7PDm8ORbkTDpMOzal7DpsKhwqJHw5PCp8KqTcONwoVHw5XDsQBbwoU4R3rCoMOSRwEaw6bClsO/woY/U1LChS7DmsKCHw==',
        '审判程序': '', '案号': '（2017）最高法执监206号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，本案的焦点问题是，双方当事人私下达成和解协议并履行完毕，是否能视为达成执行和解协议并履行完毕，本案能否恢复执行。&#xA;首先，根据《最高人民法院关于人民法院执行工作若干问题的规定（试行）》第86条的规定，在执行中，双方当事人可以自愿达成和解协议，变',
        '不公开理由': '', '案件类型': '5', '裁判日期': '2016-12-29',
        '案件名称': '广东瑞安房地产开发有限公司、平安银行股份有限公司广州黄埔大道支行金融借款合同纠纷执行审查类执行裁定书',
        '文书ID': 'DcOOwrcRw4AwDATDgcKWw6BIw6BDOMO2X8KSFMOebHIzw6DCicOXw77ClGZSGsOSay/DmcKTSG/DtcKSJDbCmQdJworDtsKjPCPDrChOIMOIWEQrw7fDgVfCiXjCs3XCuXTCr8KbZ8KlQ8ODw5kSw53DnnZdw5zDrCgdwqvCsFLCtTQfWsKbw4ElUyjDl3TCnMOTwpxswqfDp8Otw55ODH4Tw6hJw5oIwrc9BGLCpcOyScO9wrfDnsKjJcODWgjCr8KGwq03w73CjQ8=',
        '审判程序': '', '案号': '（2016）最高法执监445号', '法院名称': '最高人民法院'}, {
        '裁判要旨段原文': '本院认为，本案的争议焦点为：一、（2014）唐执字第190号责令协助单位追款通知书、（2014）唐执字第190-2号及（2014）唐执字第190-3号执行裁定是否已被23号裁定撤销；二、荣盛公司向二建公司支付工程款的行为是否违反了（2013）唐民初字第222-',
        '不公开理由': '', '案件类型': '5', '裁判日期': '2016-12-19', '案件名称': '唐山荣盛房地产开发有限公司、唐山市丰润区瑞昌商贸有限公司买卖合同纠纷执行审查类执行裁定书',
        '文书ID': 'FcKMwrkBBDEIw4Raw6LDswAhGMOTf0nCt8KXKMKSw4QHwooZV8OGwpzCpsK8bT3DsMO7woHDnyZ2MggrdMOnwr45woNFHxRHwosYXcOqSGjCpR0KDl/CscKZw4zDjTcaFy/CqkfDocOxwojCjMOCw7luwrZLw6/CoMK/F8Knw7jDmcO1w5NpTsKtWcOQPX/DrcKZwq4Fe8K3w5UjB1FteFXDtsOLwq/CiMKZLcKKw7IaNSNmwrQ6w4ISZVN9VXpEH8Ksw6UH',
        '审判程序': '', '案号': '（2016）最高法执监240号', '法院名称': '最高人民法院'}]
    run_eval = data[0]['RunEval']
    for i in range(1, len(data)):
        id = data[i]['文书ID']
        get_detail_info(runeval=run_eval, docid=id)
        break
