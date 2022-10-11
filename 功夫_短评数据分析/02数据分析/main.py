# -*- coding: utf-8 -*-
# from pylab import *
# import matplotlib.pyplot as plt
# from datetime import datetime
# import pandas as pd
# #绘图显示中文字体和负号
# plt.rcParams['font.sans-serif'] = ['SimHei']
# myfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf')
# plt.rcParams['axes.unicode_minus'] = False
# font1 = {'family' : 'Times New Roman', 'weight' : 'normal', 'size' : 22}
#
#
# #时间间隔 幂律分布
# if __name__ == '__main__':
#     pl_data = pd.read_csv("data1.csv", encoding="gbk")
#     PLTimeList = [] #评论时间列表
#     Period= [] #时间间隔
#     PeriodSeconds = []
#     times = pl_data['ctime']
#     #获取时间
#     for t in times:
#         PLTimeList.append(datetime.strptime(str(t),"%Y--%m--%d %H:%M:%S"))
#
#     PLTimeList.sort() #时间排序
#     PLTimeList.reverse() #列表中元素反向
#     #获取时间间隔再赋值给列表
#     l = len(PLTimeList)
#
#     for i in range(0, l-1):
#        cnt = (PLTimeList[i]-PLTimeList[i+1])
#        Period.append(cnt)
#     #获取秒
#     for i in Period:
#         PeriodSeconds.append(i.seconds)
#
#     #myset是另外一个列表,里面的内容是mylist里面的无重复项
#     x = []
#     y = []
#     myset = set(PeriodSeconds)
#     for item in myset:
#         x.append(item)
#         # 出现数量
#         y.append(PeriodSeconds.count(item))
#
#     #绘图
#     plt.subplot(111)
#     plt.plot(x, y,'ko')
#     plt.yscale('log')
#     plt.ylabel('P', font1)
#     plt.xlabel('timespan', font1)
#     plt.xscale('log')
#     plt.ylim(0.5,20)
#     #plt.xlim(0.001,)
#     plt.show()
import pandas as pd
from pyecharts import Pie, Line, Scatter
import os
import numpy as np
import jieba
import jieba.analyse
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from PIL import Image
font = FontProperties(fname=r'C:/Windows/Fonts/simfang.ttf')  # ,size=20指定本机的汉字字体位置


datas = pd.read_csv('data1.csv', encoding='gbk')

"""
描述性分析
# """
# 评分
# version <1.0
scores = datas.score.groupby(datas['score']).count()
pie= Pie("评分", title_pos='center', width=900)
pie.add(
    "评分",
    ['一星', '二星', '三星', '四星', '五星'],
    scores.values,
    radius=[40, 75],
    #    center=[50, 50],
    is_random=True,
    #    radius=[30, 75],
    is_legend_show=False,
    is_label_show=True,
)
pie.render('评分.html')


datas['dates'] = datas.ctime.apply(lambda x:pd.Timestamp(x).date())
datas['time'] = datas.ctime.apply(lambda x:pd.Timestamp(x).time().hour)
num_date = datas.uname.groupby(datas['dates']).count()
# 评论数时间分布
chart = Line("评论数时间分布")
chart.use_theme('dark')
chart.add( '评论数时间分布',num_date.index, num_date.values, is_fill=False, line_opacity=0.2,
          area_opacity=0.4, symbol=None)

chart.render('评论时间分布.html')

# 好评字数分布
datalikes = datas.loc[datas.likes > 5]
datalikes['num'] = datalikes.content.apply(lambda x: len(x))
chart = Scatter("likes")
chart.use_theme('dark')
chart.add('likes', np.log(datalikes.likes), datalikes.num, is_visualmap=True,
          xaxis_name='log(评论字数)',

          )
chart.render('好评字数分布.html')

texts = ';'.join(datas.content.tolist())
cut_text = " ".join(jieba.cut(texts))
# TF_IDF
keywords = jieba.analyse.extract_tags(cut_text, topK=500, withWeight=True, allowPOS=('a','e','n','nr','ns'))
text_cloud = dict(keywords)
# pd.DataFrame(keywords).to_excel('关键词前500.xlsx')

wc = WordCloud(# FFFAE3
    background_color="white",  # 设置背景为白色，默认为黑色
    width=400,  # 设置图片的宽度
    height=600,  # 设置图片的高度
    random_state = 2,
    max_font_size=500,  # 显示的最大的字体大小
    font_path="STSONG.TTF",
).generate_from_frequencies(text_cloud)
# 为图片设置字体

# 图片背景
#bg_color = ImageColorGenerator(bg)
#plt.imshow(wc.recolor(color_func=bg_color))
plt.imshow(wc)
# 为云图去掉坐标轴
plt.axis("off")
plt.show()
wc.to_file("词云.png")