__author__  =  'FWJ' 
__time__  =  '2018-11-07 09:58:52' 

from fake_useragent import UserAgent
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import requests
# import traceback


class LianJiaSpider(object):
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {"User-Agent": self.ua.random}
        self.datas = list()

    def get_max_page(self, url):
        '''
        抓取当前页最大页数，就是页面底下显示页面总数的位置
        '''
        reponse = requests.get(url, headers=self.headers)
        if reponse.status_code == 200:
            source = reponse.text
            soup = BeautifulSoup(source, 'html.parser')
            a = soup.find_all("div", class_="page-box house-lst-page-box")
            max_page = eval(a[0].attrs["page-data"])["totalPage"]
            return max_page

        else:
            print("请求失败 statue: {}".format(reponse.status_code))
            return None
    
    def pares_page(self, url):
        max_page = self.get_max_page(url)
        for i in range(1, max_page + 1):
            url = 'https://gz.lianjia.com/zufang/pa{}/'.format(i)
            
            print("当前正在爬取： {}".format(url))
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            a = soup.find_all("div", class_="info-panel")

            for j in range(len(a)):
                try:
                    link = a[j].find("a")["href"]
                    print(link)
                    detail = self.parse_detail(link)
                    self.datas.append(detail)
                except:
                    print('get page link is fail')
                    # print('tracekback.print_exc():',traceback.print_exc())
                    continue
            print("所有数据爬取完成，正在存储到csv文件中")

            data = pd.DataFrame(self.datas)
            data.to_csv("链家网租房数据.csv", encoding='utf_8_sig')


    def parse_detail(self, url):
        detail = {}
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            b = soup.find("div", class_="content zf-content")
            detail["月租金"] = int(b.find("span", class_="total").text.strip())
            detail["面积"] = b.find_all("p", class_="lf")[0].text[3:].strip()
            detail["房屋户型"] = b.find_all("p", class_="lf")[1].text[5:].strip()
            detail["楼层"] = b.find_all("p", class_="lf")[2].text[3:].strip()
            detail["房屋朝向"] = b.find_all("p", class_="lf")[3].text[5:].strip()
            detail["地铁"] = b.find_all("p")[4].text[3:].strip()
            detail["小区"] = b.find_all("p")[5].text[3:].split('-')[0].strip()
            detail["位置"] = b.find_all("p")[6].text[3:].strip()
            return detail
        else:
            print("请求失败 statue: {}".format(response.status_code))
            return None


if __name__ == '__main__':
    url = "https://gz.lianjia.com/zufang/"
    spider = LianJiaSpider().pares_page(url)
        

    

    
