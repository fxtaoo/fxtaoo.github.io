#!/usr/bin/env python3
# coding:utf-8

import time
import os
import subprocess
import datetime
from PIL import Image
from pypinyin import lazy_pinyin

SORT_LIST = (
    ("#闲聊", "chat.md"),
    ("#笔记", "note.md"),
    ("#Go", "go.md"),
    ("#Dev", "dev.md"),
    ("#Ops", "ops.md")
)

# 在 REAMDE.md 插入新文章链接
reademe_insert_new_article_link = 7
domain_name = "https://fangxuetao.com/"
date = time.strftime("%Y/%m/%d", time.localtime())

article_name = input("\n输入文章名：")

# 移除文章名指定字符
remove_char = ["《", "》", " ", "，", ",", "。", "!", "！", ".", "、"]
file_name = ""
for char in article_name:
    if char not in remove_char:
        file_name += char
# 转拼音
file_name = lazy_pinyin(file_name)

# 输出并选择类别
sort_number = 0
for sort in SORT_LIST:
    sort_number += 1
    print(str(sort_number) + "." + sort[0] + "  ", end="")
    if sort_number % 5 == 0:
        print("")
input_sort_list = input("\n\n输入类别数字序号（多选空格分隔）：").strip().split()

# 文件名
article_flename = time.strftime("%Y-%m-%d", time.localtime())
for word in file_name:
    article_flename += "-" + word
image_dir_name = article_flename
article_flename += ".md"

# 文章文件夹路径为 ./_posts/类别/年/
path_sort = (SORT_LIST[[int(input_sort_list[0])-1][0]][1][0:-3])
article_file_dir_path = f"_posts/{path_sort}/{datetime.datetime.now().year}"

# 检查文件夹是否存在，不存在递归创建
if not os.path.exists(article_file_dir_path):
    os.makedirs(article_file_dir_path)
article_file_path = f"{article_file_dir_path}/{article_flename}"

article_sort_info = ""
articl_link = (
    "["
    + date
    + " "
    + article_name
    + "]("
    + domain_name
    + article_flename[11:-3]
    + ")  "
)

for sort in input_sort_list:
    # 文章类别信息
    article_sort_info += (
        f"[`{SORT_LIST[int(sort) - 1][0]}`]({domain_name}{SORT_LIST[int(sort) - 1][1][0:-3]}) ")
    # 类别导航目录
    sort_file_path = (f"_posts/1970-01-01-{SORT_LIST[int(sort) - 1][1]}")
    # 新文章链接写入到对应类别中
    shell_cmd = f"sed -i '7i {articl_link}' {sort_file_path}"
    subprocess.call([shell_cmd], shell=True, encoding=None)

# 当前文章页参数
open(article_file_path, mode="ab+").write((f"---\ntitle: {article_name}\n---\n\n## {article_name} <!-- omit in toc -->\n\n{article_sort_info}\n\n*{date}*\n\n").encode("utf-8")
                                          )

# 文章链接添加到 README.md
shell_cmd = f"sed -i '{reademe_insert_new_article_link}i {articl_link}' README.md"
subprocess.call([shell_cmd], shell=True, encoding=None)


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
    image_dir_path = f"assets/images/{path_sort}/{image_dir_name}"
    os.makedirs(image_dir_path)
    num = 0
    for i in find_all_file(image_tmp_path):
        im = Image.open(i)
        image_name = f"fangxuetao.com-{image_dir_name}-{num}.webp"
        num += 1
        im.save(f"{image_dir_path}/{image_name}", 'webp')
        image_url_list += f"![{image_name}](/{image_dir_path}/{image_name})\n\n"
        os.remove(i)

    shell_cmd = f"echo '{image_url_list}' >> {article_file_path}"
    subprocess.call([shell_cmd], shell=True, encoding=None)

# vscode 打开新建的文章
os.system("code " + article_file_path)
