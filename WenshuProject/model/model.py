# -*- coding: utf-8 -*-

import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
from sqlalchemy import Column, String, Integer, Text, DateTime, INT, DATE, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from model import db_config

Base = declarative_base()


class XZCF(Base):
    """
    table:行政处罚
    """
    __tablename__ = 'tb_xzcf'

    id = Column(Integer, primary_key=True)
    data_source = Column(String(70), default='', comment='来源')  # 来源
    case_name = Column(String(200), comment='案件名称')  # 案件名称
    case_no = Column(String(50), comment='行政处罚决定书文号')  # 行政处罚决定书文号
    case_cate = Column(String(200), comment='处罚类别')  # 处罚类别
    case_reason = Column(Text(), comment='处罚事由')  # 处罚事由
    case_base = Column(Text(), comment='处罚依据')  # 处罚依据
    name = Column(String(225), comment='行政相对人名称')  # 行政相对人名称
    unique_code = Column(String(225), comment='统一社会信用代码')  # 统一社会信用代码
    org_code = Column(String(50), comment="组织机构代码")  # 统一社会信用代码
    gs_code = Column(String(225), comment='工商登记号')  # 工商登记号
    tax_code = Column(String(100), comment='税务登记号')  # 税务登记号

    punish_effected_date = Column(String(50), comment="处罚生效期")  # 处罚生效期
    punish_closing_date = Column(String(50), comment="处罚截止期")  # 处罚截止期
    taxpayer_id = Column(String(50), comment='纳税人识别号')  # 纳税人识别号

    admin_cardno = Column(String(100), comment="行政相对人居民身份证号")  # 行政相对人居民身份证号
    public_limit = Column(String(100), comment="公示期限")  # 公示期限
    data_update_date = Column(String(50), comment="数据更新日期")  # 数据更新日期
    local_code = Column(String(50), comment="地方编码")  # 地方编码

    legal_name = Column(String(100), comment='法定代表人姓名')  # 法定代表人姓名
    id_card = Column(String(50), comment='法定代表人身份证号码')  # 法定代表人身份证号码
    cf_result = Column(Text(), comment='处罚结果')  # 处罚结果
    cf_gov = Column(String(50), comment='处罚机关')  # 处罚机关
    current_status = Column(String(20), comment='当前状态')  # 当前状态
    punish_date = Column(String(20), default='', comment='处罚日期')  # 处罚日期
    crawl_time = Column(DateTime(), default=datetime.now(), comment='爬取时间')  # 爬取时间

    hash = Column(String(100), default='', unique=True, comment="hash值用于排重")

    case_tax_type = Column(String(100), default="", comment="税收违法类型")


class Credit(Base):
    """
    table:纳税信用评级
    """
    __tablename__ = 'tb_credit'

    id = Column(Integer, primary_key=True)
    data_source = Column(String(70), default='', comment='来源')  # 来源
    name = Column(String(200), unique=True, comment='公司名字')  # 公司名字
    reco_code = Column(String(200), comment='纳税人识别号')  # 纳税人识别号
    credit_level = Column(String(10), default='A', comment='纳税人信用级别')  # 纳税人信用级别
    which_state = Column(String(200), comment='所属分局')  # 所属分局
    which_year = Column(String(50), comment='年份')  # 年份
    crawl_time = Column(DateTime(), default=datetime.now())  # 抓取时间
    update_time = Column(DateTime(), comment='更新时间')  # 更新时间

    __table_args__ = (
        UniqueConstraint('name', 'which_year', name='uix_name_year'),  # 联合唯一索引
        Index('ix_name_year', 'name'),  # 联合索引
    )


class WFAJ(Base):
    """
    table:重大税收违法案件
    """
    __tablename__ = 'tb_wfaj'

    id = Column(Integer, primary_key=True)
    data_source = Column(String(70), default='')
    name = Column(String(200), comment='纳税人名称')  # 纳税人名称
    reco_code = Column(String(200), comment='纳税人识别号或社会信用代码')  # 纳税人识别号或社会信用代码
    org_code = Column(String(100), comment='组织机构代码')  # 组织机构代码
    case_property = Column(String(200), comment='案件性质')  # 案件性质
    address = Column(String(200), comment='注册地址')  # 注册地址
    legal_man = Column(String(200), comment='违法期间法人代表或者负责人姓名、性别及身份证号码（或其他证件号码）')  # 违法期间法人代表或者负责人姓名、性别及身份证号码（或其他证件号码）

    case_base = Column(String(1000), comment='主要违法事实相关法律依据及税务处理处罚情况', unique=True)  # 主要违法事实相关法律依据及税务处理处罚情况

    finace_man = Column(String(300), comment='负有直接责任的财务负责人姓名、性别、证件名称及号码')
    agency_man = Column(String(300), comment="负有直接责任的中介机构信息及其从业人员信息")

    cf_result = Column(String(1000), comment="相关法律依据及税务处理处罚情况")

    update_time = Column(DateTime(), comment='案件发布时间')  # 案件发布时间
    crawl_time = Column(DateTime(), default=datetime.now(), comment='抓取时间')  # 抓取时间


class QSGG(Base):
    """
    table:欠税公告
    """
    __tablename__ = 'tb_qsgg'

    id = Column(Integer, primary_key=True)
    data_source = Column(String(70), default='', comment='来源')  # 来源
    address = Column(String(200), comment='经营地点')  # 经营地点
    card_type = Column(String(20), comment="证件种类")  # 证件种类
    card_id = Column(String(50), comment='证件号码')  # 证件号码
    company = Column(String(50), comment='公司名称,纳税人名称')  # 公司名称
    detail_link = Column(String(200), comment='详情链接')  # 详情链接
    identity_num = Column(String(100), comment='纳税人识别号')  # 纳税人识别号
    name = Column(Text(), comment='负责人姓名')  # 负责人姓名
    new_tax_amount = Column(String(20), comment='当前新发生的欠税余额')  # 当前新发生的欠税余额
    publish_org = Column(String(20), comment='发布单位,主管税务机关')  # 发布单位
    publish_time = Column(String(20), comment='发布时间')  # 发布时间
    spider_time = Column(DateTime(), comment='爬取时间')  # 爬取时间
    tax_amount = Column(String(20), comment='欠税余额')  # 欠税余额
    tax_type = Column(Text(), comment='欠税税种')  # 欠税税种
    taxpayer_type = Column(String(20), comment='纳税人类型')  # 纳税人类型

    cur_status = Column(String(50), comment="当前状态")  # 当前状态


Base.metadata.create_all(db_config.engine)
