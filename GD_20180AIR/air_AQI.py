__author__  =  'FWJ' 
__time__  =  '2018-11-27 16:10:17' 
import time
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
import numpy as np
import pandas as pd
from pyecharts import Line

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

def citys(province, year):
    '''
    城市爬取
    '''
    cities = []
    cities_pinyin = []
    aqiurl = 'http://www.tianqihoubao.com/aqi/'
    response = requests.get(url=aqiurl, headers=headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, 'lxml')
    b = soup.original_encoding

    provinces = soup.find('div', class_="citychk")

    for bt in provinces.find_all('dl'):
        b = bt.find('b').get_text()
        if b == province:
            dd = bt.find('dd')
            for a in dd.find_all('a'):
                city = a.get_text().strip()
                cities.append(city)
                city_pinyin = pinyin(city)
                cities_pinyin.append(city_pinyin)
    
    AQI(cities, cities_pinyin, year)
    


def AQI(cities, cities_pinyin, year):
    v = []
    for i in range(len(cities)):
        filename = 'air_' + cities_pinyin[i] + '_' + str(year) + '.csv'
        df = pd.read_csv(filename, header=None, names=["Date", "Quality_grade", "AQI", "AQI_rank", "PM"])
        dom = df[['Date', 'AQI']]
        list1 = []
        for j in dom['Date']:
            time = j.split('-')[1]
            list1.append(time)
        df['month'] = list1

        month_message = df.groupby(['month'])
        month_com = month_message['AQI'].agg(['mean'])
        print(month_message['AQI'])
        print(month_com)
        month_com.reset_index(inplace=True)
        print(month_com)
        month_com_last = month_com.sort_index()

        print(type(month_com_last['mean']))
        v1 = np.array(month_com_last['mean'])
        v1 = ["{}".format(int(i)) for i in v1]
        v.append(v1)

    attr = ["{}".format(str(i) + '月') for i in range(1, 12)]

    line = Line("广东省AQI全年走势图", title_pos='centos', title_top='0', width=2500, height=1520)
    a = 0

    for city in cities:
        line.add(city, attr, v[a], legend_top='8%')
        a = a + 1
    line.render("2018年广东省AQI全年走势图.html")


def pinyin(city):
    '''
    汉字转换拼音
    '''
    city_pinyin = "".join(lazy_pinyin(city))
    return city_pinyin



citys('广东', 2018)