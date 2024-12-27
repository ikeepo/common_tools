#!/bin/bash

# 获取输入参数
input="$1"

# 如果没有输入参数，显示错误并退出
if [ -z "$input" ]; then
  echo "请提供一个文件或目录作为输入参数。"
  exit 1
fi

# 如果输入的是目录路径
if [ -d "$input" ]; then
  echo "you specify a directory path $input"
  # 删除所有Zone.Identifier文件
  find "$input" -type f -name "*:Zone.Identifier" -exec rm -f {} \;
  # echo "删除所有Zone.Identifier文件"
  # 遍历目录中的所有文件
  for file in "$input"/*; do
    if [ -f "$file" ]; then
      # 获取文件名
      filename=$(basename "$file")
      # 删除文件名中的空格
      modified_filename=$(echo "$filename" | tr -d '[:space:]')
      # delete () and []
      modified_filename=$(echo "$modified_filename" | sed 's/(\|)//g')
      modified_filename=$(echo "$modified_filename" | sed 's/\[//g')
      modified_filename=$(echo "$modified_filename" | sed 's/\]/_/g')
      # 删除-libgen.li
      modified_filename=$(echo "$modified_filename" | sed 's/-libgen.li//g')
      modified_filename=$(echo "$modified_filename" | sed 's/libgen.li//g')
      #echo "修改后名称为$modified_filename"
      # 将文件名中的 | 或者 ｜ 替换为 _
      modified_filename=$(echo "$modified_filename" | sed 's/|/_/g')
      modified_filename=$(echo "$modified_filename" | sed 's/｜/_/g')
      modified_filename=$(echo "$modified_filename" | sed 's/／/_/g')
      modified_filename=$(echo "$modified_filename" | sed 's//_/g')
      # 全角替换为半角
      modified_filename=$(echo "$modified_filename" | nkf -Z1 -w)
      #echo "修改后名称为$modified_filename"
      # 如果文件名被修改，则重命名文件
      if [ "$filename" != "$modified_filename" ]; then
        mv "$file" "$input/$modified_filename"
        echo "🆗 name change: $filename ---> $modified_filename"
      else
        echo "👍 no need change: $filename "

      fi
    fi
  done

# 如果输入的是文件路径
elif [ -f "$input" ]; then
  echo "you specify a file name $input"
  # 遍历目录中的所有文件
  # 获取文件名
  filename=$(basename "$input")

  # 将文件名中的 | 替换为 _
  modified_filename=$(echo "$filename" | sed 's/|/_/g')

  # 如果文件名被修改，则重命名文件
  if [ "$filename" != "$modified_filename" ]; then
    mv "$input" "$(dirname "$input")/$modified_filename"
    echo "已重命名: $filename -> $modified_filename"
  fi

else
  echo "输入的路径无效: $input"
  exit 1
fi
