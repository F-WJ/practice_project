__author__  =  'FWJ' 
__time__  =  '2018-11-24 17:00:26' 
import time
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

def citys(province, year):
    '''
    城市爬取
    '''
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
                city = a.get_text()
                aqihref = a.get('href').replace('.html', '')
                cityair(city, aqihref, year)
                # print(a.get_text())
                # print(a.get('href').replace('.html', ''))



def cityair(city, aqihref, year):
    '''
    空气质量数据
    '''
    for i in range(1, 13):
        time.sleep(2)
        url = 'http://www.tianqihoubao.com/' + aqihref + '-' + str(year) + str('%02d' %i) + '.html'
        print(url)
        response = requests.get(url=url, headers=headers)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text, 'lxml')
        tr = soup.find_all('tr')
        text = tr[1:]
        for j in tr[1:]:
            td = j.find_all('td')
            Date = td[0].get_text().strip()
            Quality_grade = td[1].get_text().strip()
            AQI = td[2].get_text().strip()
            AQI_rank = td[3].get_text().strip()
            PM = td[4].get_text()

            city_pinyin = pinyin(city).strip()
            filename = 'air_' + city_pinyin + '_' + str(year) + '.csv'
            with open(filename, 'a+', encoding='utf-8-sig') as f:
                f.write(Date + ',' + Quality_grade + ',' + AQI + ',' + AQI_rank + ',' + PM + '\n')


def pinyin(city):
    '''
    汉字转换拼音
    '''
    city_pinyin = "".join(lazy_pinyin(city))
    return city_pinyin


citys('广东', 2018)






