#!/usr/bin/env bash
echo "start spider....."
nohup python w_xingshi.py > wenshu_log/xinshi.log 2>&1 &
nohup python w_minshi.py > wenshu_log/minshi.log 2>&1 &
nohup python w_xingzheng.py > wenshu_log/xingzheng.log 2>&1 &
nohup python w_peichang.py > wenshu_log/peichang.log 2>&1 &
nohup python w_zhixing.py > wenshu_log/zhixing.log 2>&1 &