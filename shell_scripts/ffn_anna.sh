#!/bin/bash 
# Anna-Archive文件名修改
# Usage: ./rename_epub.sh <folder>

FOLDER="$1"

if [ -z "$FOLDER" ]; then
    echo "请提供文件夹路径"
    exit 1
fi

# 遍历文件夹内所有 .epub
find "$FOLDER" -type f -name "*.epub" | while read -r FILE; do
    BASENAME=$(basename "$FILE")
    DIRNAME=$(dirname "$FILE")

    # 按 "--" 分割，取第 0 部分
    PART0=$(echo "$BASENAME" | awk -F '--' '{print $1}')

    # 去掉结尾的空格
    PART0=$(echo "$PART0" | sed 's/[[:space:]]*$//')

    NEWNAME="${PART0}.epub"

    # 重命名
    mv "$FILE" "$DIRNAME/$NEWNAME"

    echo "Renamed:"
    echo "  $BASENAME"
    echo "  → $NEWNAME"
    echo
done
