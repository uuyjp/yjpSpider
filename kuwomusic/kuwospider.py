# !/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: yjp
# @software: PyCharm
# @file: kuwospider.py
# @time: 2022-09-18 16:18
import os
from requests_html import HTMLSession
import requests
import execjs
session = HTMLSession()

class kuwoSpider(object):
    def __init__(self):
        # 先写一页测试一下
        # self.start_url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
        self.start_url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key=%E9%9E%A0%E5%A9%A7%E7%A5%8E&pn=1&rn=30&httpsStatus=1&reqId={}"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1663489177; _ga=GA1.2.384465248.1663489177; _gid=GA1.2.815458413.1663489177; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1663494020; kw_token=ZJ8122YWTFS',
            'csrf': 'ZJ8122YWTFS',
            'Host': 'www.kuwo.cn',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E9%9E%A0%E5%A9%A7%E7%A5%8E',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        self.play_url = "http://www.kuwo.cn/api/v1/www/music/playUrl?mid={}&type=music&httpsStatus=1&reqId={}"
    def parse_start_url(self):
        start_url = self.start_url.format(self.get_reqId())
        response = session.get(start_url,headers=self.headers).json()
        self.parse_start_response(response)
        # self.get_reqId()
    def parse_start_response(self,response):
        info_list = response["data"]["list"]
        name_list,rid_list = self.get_name_and_rid(info_list)
        self.get_video_url(name_list,rid_list)
    def get_video_url(self,name_list,rid_list):
        for name,rid in zip(name_list,rid_list):
            play_url = self.play_url.format(rid, self.get_reqId())
            resp = session.get(play_url,headers=self.headers).json()
            try:
                video_url = resp['data']['url']
                video_content = requests.get(video_url).content
                self.download_mp3(name,video_content)
            except:
                with open('log_fail.txt', 'a+') as f:
                    f.write("{}=>下载失败\n".format(name))
    def download_mp3(self,name,video_content):
        os_path = os.getcwd() + '/歌曲/'
        if not os.path.exists(os_path):
            os.mkdir(os_path)
        with open(os_path + f'{name}' + '.mp3','wb') as f:
            f.write(video_content)
        print("{}下载完成".format(name))
        with open('log_success.txt', 'a+') as f:
            f.write("{}=>下载完成\n".format(name))
    def get_name_and_rid(self,info_list):
        """
        提取info_list中的rid和name
        :param info_list:
        :return:
        """
        name_list = []
        rid_list = []
        for item in info_list:
            name_list.append(item['name'])
            rid_list.append(item['rid'])
        return name_list,rid_list
    def get_reqId(self):
        with open("reqId.js",'r') as f:
            data = f.read()
        jscode = execjs.compile(data)
        reqId = jscode.call('reqId')
        # print(reqId)
        return reqId
if __name__ == '__main__':
    k = kuwoSpider()
    k.parse_start_url()