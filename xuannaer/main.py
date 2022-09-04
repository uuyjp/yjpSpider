# !/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: yjp
# @software: PyCharm
# @file: main.py
# @time: 2022-09-04 18:47
import requests
import re
from fontTools.ttLib import TTFont
from lxml import etree
index_url = "https://www.xuanzhi.com/zhaopaigua"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
response = requests.get(index_url,headers=headers).content.decode()
woff = re.findall("https://img2.xuannaer.com/static/new/fonts/\w{16}/font.woff\?\d{11}",response,re.S)[0]
woff_bytes = requests.get(woff,headers=headers,allow_redirects=True).content
with open("zhaopaigua.woff","wb") as f:
    f.write(woff_bytes)
font = TTFont('zhaopaigua.woff')
font.saveXML('zhaopaigua.xml')
with open('zhaopaigua.xml','r',encoding="utf-8") as f:
    document = f.read()
cmap = re.findall('<map code="(.*?)" name="*(.*?)"/>',document,re.S)
item = {}
for node in cmap:
    item[node[1]] = chr(eval(node[0]))
# print(item)
result ={}
GlyphID = re.findall('<GlyphID id="(\d+)" name="(.*?)"/>',document,re.S)[1:]
for node in GlyphID[:10]:
    num = int(node[0]) - 1
    result[item[node[1]]] = num
print(result)

html_str = etree.HTML(response)
# print(response)
title_list  = re.findall('target="_blank" title="(.*?)" class="title-link',response)
square_list = html_str.xpath("//*[@class='xn-cf']/text()")
print(square_list)
# for title in title_list:
#     print(title)
