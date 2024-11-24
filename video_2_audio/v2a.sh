#!/bin/bash

# 激活虚拟环境
echo "正在激活虚拟环境..."
source .v2a/bin/activate
if [ $? -ne 0 ]; then
    echo "激活虚拟环境失败，退出。"
    exit 1
fi
echo "虚拟环境已激活。"

# 运行 option_daily_data.py
echo "正在运行 video2audio.py ..."
python video2audio.py
if [ $? -ne 0 ]; then
    echo "运行 video2audio.py 失败，退出。"
    exit 1
fi
echo "video2audio.py 运行成功。"

