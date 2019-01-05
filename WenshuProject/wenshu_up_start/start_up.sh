#!/usr/bin/env bash
echo "start spider....."
nohup python start_dxingshi.py > wenshu_up_log/xinshi.log 2>&1 &
nohup python start_dminshi.py > wenshu_up_log/minshi.log 2>&1 &
nohup python start_dxingzheng.py > wenshu_up_log/xingzheng.log 2>&1 &
nohup python start_dpeichang.py > wenshu_up_log/peichang.log 2>&1 &
nohup python start_dzhixing.py > wenshu_up_log/zhixing.log 2>&1 &