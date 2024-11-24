#!/bin/bash

# 激活虚拟环境
echo "正在激活虚拟环境..."
source .ytb_dl/bin/activate
if [ $? -ne 0 ]; then
    echo "激活虚拟环境失败，退出。"
    exit 1
fi
echo "虚拟环境已激活。"

# 运行 option_daily_data.py
echo "正在运行 dl.py ..."
python dl.py
if [ $? -ne 0 ]; then
    echo "运行 dl.py 失败，退出。"
    exit 1
fi
echo "dl.py 运行成功。"

