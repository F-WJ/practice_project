__author__  =  'FWJ' 
__time__  =  '2018-11-27 11:41:13' 
from pypinyin import pinyin, lazy_pinyin, Style
import requests

a = '佛山'

print("".join(lazy_pinyin(a)))


for x in []:
    print(x)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

def citys():
    '''
    城市爬取
    '''
    aqiurl = 'http://www.tianqihoubao.com/aqi/'
    response = requests.get(url=aqiurl, headers=headers)
    print(response.encoding)

citys()