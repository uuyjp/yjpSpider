# !/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: yjp
# @software: PyCharm
# @file: main.py
# @time: 2022-09-30 22:57
import sys
import os
import xlwt
import xlrd
from xlutils.copy import copy
from requests_html import HTMLSession
import time
from threading import *
sys.setrecursionlimit(3000)  # 将默认的递归深度修改为3000
session = HTMLSession()

class plSpider(object):
    def __init__(self):
        self.start_url = "https://api.bilibili.com/pgc/review/short/list?media_id=28227820&ps=20&sort=0&cursor={}"
        self.headers = {
            "cookie": "buvid3=BB7FFBF9-7220-4054-BD27-9E2B59ED908E34751infoc; rpdid=|(u|JJRRY|Rk0J'uYku~lku|J; LIVE_BUVID=AUTO5016226178557228; video_page_version=v_old_home; fingerprint_s=ff4b2ef3470a91c32417af22e8d5a16b; buvid4=01D09AFB-B416-4588-6D03-9AD185A2ADBD39820-022012515-gGjJrmXHf7W+R9pSvVQ1AQ%3D%3D; buvid_fp_plain=undefined; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; b_ut=5; DedeUserID=666724842; DedeUserID__ckMd5=c4d1c388ea2a797b; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=9aae7dbb9720c962cc9f3cfea08fe04d; _uuid=A7319F1B-DE3C-D83F-7E2D-6C7D281366FE51671infoc; fingerprint=cf3ceab8e58b4ea6b330ce7f4d50a98d; is-2022-channel=1; SESSDATA=34d581c1%2C1675995117%2C62be9%2A81; bili_jct=37ec38df20e12788ced5a8c122112a80; sid=6doufkax; blackside_state=1; CURRENT_QUALITY=80; buvid_fp=cf3ceab8e58b4ea6b330ce7f4d50a98d; b_nut=100; CURRENT_FNVAL=4048; bp_video_offset_666724842=711734750365089800; innersign=1; b_lsid=F57AB54F_1838F20A1CE; PVID=1",
            'user-agent' : 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        self.cnt = 0
    def parse_start_url(self):
        start_url = self.start_url.format(0)
        response = session.get(start_url,headers = self.headers).json()
        self.parse_start_response(response)
    def parse_start_response(self,response):
        data = response["data"]['list']
        cursor = response["data"]["next"]
        self.parse_data(data)
        self.get_next_url(cursor)
    def get_next_url(self,cursor):

        next_url = self.start_url.format(cursor)
        response = session.get(next_url, headers=self.headers).json()
        self.parse_next_response(response)
    def parse_next_response(self,response):
        data = response["data"]['list']
        cursor = response["data"]["next"]
        if cursor == 0:
            exit(0)
        self.parse_data(data)
        self.get_next_url(cursor)
    def parse_data(self,data):
        """
        提取 uname,score,disliked,liked,likes,ctime,content
        :param data:
        :return:
        """

        for item in data:
            self.cnt += 1
            print(f"{self.cnt}")
            uname = item['author']['uname']
            content = item['content']
            score = item['score']
            ctime = item['ctime']
            timeArray = time.localtime(int(ctime))
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            disliked, liked, likes = item["stat"]["disliked"],item["stat"]["liked"],item["stat"]["likes"]
            dict = {
                '评论数据':[uname,score,disliked,liked,likes,otherStyleTime,content]
            }
            self.save_excel(dict)
    def save_excel(self, data):
            #传入的是字典
            # data = {
            #     '基本详情': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
            # }
            os_path_1 = os.getcwd() + '/短评数据/'
            if not os.path.exists(os_path_1):
                os.mkdir(os_path_1)
            # os_path = os_path_1 + self.os_path_name + '.xls'
            os_path = os_path_1 + '功夫短评数据2.xls'
            if not os.path.exists(os_path):
                # 创建新的workbook（其实就是创建新的excel）
                workbook = xlwt.Workbook(encoding='utf-8')
                # 创建新的sheet表
                worksheet1 = workbook.add_sheet("评论数据", cell_overwrite_ok=True)
                borders = xlwt.Borders()  # Create Borders
                """定义边框实线"""
                borders.left = xlwt.Borders.THIN
                borders.right = xlwt.Borders.THIN
                borders.top = xlwt.Borders.THIN
                borders.bottom = xlwt.Borders.THIN
                borders.left_colour = 0x40
                borders.right_colour = 0x40
                borders.top_colour = 0x40
                borders.bottom_colour = 0x40
                style = xlwt.XFStyle()  # Create Style
                style.borders = borders  # Add Borders to Style
                """居中写入设置"""
                al = xlwt.Alignment()
                al.horz = 0x02  # 水平居中
                al.vert = 0x01  # 垂直居中
                style.alignment = al
                # 合并 第0行到第0列 的 第0列到第13列
                '''基本详情13'''
                # worksheet1.write_merge(0, 0, 0, 13, '基本详情', style)
                excel_data_1 = ('uname','score','disliked','liked','likes','ctime','content')
                for i in range(0, len(excel_data_1)):
                    worksheet1.col(i).width = 2560 * 3
                    #               行，列，  内容，            样式
                    worksheet1.write(0, i, excel_data_1[i], style)
                workbook.save(os_path)
            # 判断工作表是否存在
            if os.path.exists(os_path):
                # 打开工作薄
                workbook = xlrd.open_workbook(os_path)
                # 获取工作薄中所有表的个数
                sheets = workbook.sheet_names()
                for i in range(len(sheets)):
                    for name in data.keys():
                        worksheet = workbook.sheet_by_name(sheets[i])
                        # 获取工作薄中所有表中的表名与数据名对比
                        if worksheet.name == name:
                            # 获取表中已存在的行数
                            rows_old = worksheet.nrows
                            # 将xlrd对象拷贝转化为xlwt对象
                            new_workbook = copy(workbook)
                            # 获取转化后的工作薄中的第i张表
                            new_worksheet = new_workbook.get_sheet(i)
                            for num in range(0, len(data[name])):
                                new_worksheet.write(rows_old, num, data[name][num])
                            new_workbook.save(os_path)
    def Thread_Run(self):
        Thread(target=self.parse_start_url()).start()

if __name__ == '__main__':
    p = plSpider()
    p.Thread_Run()