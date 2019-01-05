#!/usr/bin/env bash
echo "start spider....."
nohup python ws_xingshi.py > wenshu_log/xinshi_save.log 2>&1 &
nohup python ws_minshi.py > wenshu_log/minshi_save.log 2>&1 &
nohup python ws_xingzheng.py > wenshu_log/xingzheng_save.log 2>&1 &
nohup python ws_peichang.py > wenshu_log/peichang_save.log 2>&1 &
nohup python ws_zhixing.py > wenshu_log/zhixing_save.log 2>&1 &