#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 追加图片


import os
import subprocess
from PIL import Image


SORT_LIST = (
    ("#闲聊", "chat.md"),
    ("#笔记", "note.md")
)

article_name = input("\n输入文章名：")

# 输出并选择类别
sort_number = 0
for sort in SORT_LIST:
    sort_number += 1
    print(str(sort_number) + "." + sort[1] + "  ", end="")
    if sort_number % 5 == 0:
        print("")
input_sort_list = input("\n\n输入类别数字序号（多选空格分隔）：").strip().split()
# 文章类别
path_sort = (SORT_LIST[[int(input_sort_list[0])-1][0]][1][0:-3])

# 检查 image 存在图片并处理


def find_all_file(path):
    for root, ds, fs in os.walk(path):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


# 临时图片文件夹是否有图片
image_tmp_path = f'image'
if not os.path.exists(image_tmp_path):
    os.makedirs(image_tmp_path)

if os.listdir(image_tmp_path):
    image_url_list = ''
    image_dir_path = f"assets/images/{path_sort}/{article_name}"
    if not os.path.exists(image_tmp_path):
        os.makedirs(image_tmp_path)
    num = len(os.listdir(f"{image_dir_path}"))
    for i in find_all_file(image_tmp_path):
        im = Image.open(i)
        image_name = f"fangxuetao.com-{article_name}-{num}.webp"
        num += 1
        im.save(f"{image_dir_path}/{image_name}", 'webp')
        image_url_list += f"![{image_name}](/{image_dir_path}/{image_name})\n\n"
        os.remove(i)

    shell_cmd = f"echo '{image_url_list}' >> _posts/{path_sort}/{article_name}.md"
    subprocess.call([shell_cmd], shell=True, encoding=None)
