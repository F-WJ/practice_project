__author__  =  'FWJ' 
__time__  =  '2018-12-11 09:43:00' 

import requests
import re
from lxml import etree


headers  = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}


def fix_url(url):
    return 'http:' + url

def get_css():
    '''
    爬取控制数目css文件
    '''
    url = 'http://www.dianping.com/guangzhou/ch10/g103'
    
    r = requests.get(url, headers=headers)
    content = r.content.decode("utf-8")
    matched = re.search(r'href="([^"]+svgtextcss[^"]+)', content, re.M)
    if not matched:
        raise Exception("cannot find svgtextcss file")
    css_url = matched.group(1)
    css_url = fix_url(css_url)

    get_svg(css_url)
    return css_url


def get_svg(css_url):
    '''
    爬取图片
    '''
    r = requests.get(css_url, headers=headers)
    content = r.content.decode("utf-8")
    matched = re.search(r'span\[class\^="xwu"].*?background\-image: url\((.*?)\);', content)
    if not matched:
        raise Exception("cannot find svg file")
    svg_url = matched.group(1)
    svg_url = fix_url(svg_url)
    r = requests.get(svg_url, headers=headers)
    content = r.content.decode("utf-8")
    print(content)
    matched = re.search(r'.*?>(\d+)</text>', content)
    if not matched:
        raise Exception("cannot find digits")
    digits = list(matched.group(1))
    return digits

def get_class_offset(css_url):
    r = requests.get(css_url, headers=headers)
    content = r.content.decode("utf-8")
    matched = re.findall(r'(\.[a-zA-Z0-9-]+)\{background:(\-\d+\.\d+)px', content)
    result = {}
    for item in matched:
        css_class = item[0][1:]
        offset = item[1]
        result[css_class] = offset
    return result
    
def get_review_num(page_url, class_offset, digits):
    '''
    爬取所需信息
    '''
    r = requests.get(page_url, headers=headers)
    content = r.content.decode("utf-8")
    root = etree.HTML(content)
    shop_nodes = root.xpath('.//div[@id="shop-all-list"]/ul/li')
    for shop_node in shop_nodes:
        name_node = shop_node.xpath('.//div[@class="tit"]/a')[0]
        name = name_node.attrib["title"]
        review_num_node = shop_node.xpath('.//div[@class="comment"]/a[@class="review-num"]/b')[0]
        num = 0
        if review_num_node.text:
            num = num * 10 + int(review_num_node.text)
        for digit_node in review_num_node:
            css_class = digit_node.attrib["class"]
            offset = class_offset[css_class]
            index = int((float(offset)+7)/-12)
            digit = int(digits[index])
            num = num * 10 + digit
        last_digit = review_num_node[-1].tail
        if last_digit:
            num = num * 10 + int(last_digit)
        
        print("restaurant: {}, review num: {}".format(name, num))


css_url = get_css()
digits = get_svg(css_url)
class_offset = get_class_offset(css_url)
url = "http://www.dianping.com/guangzhou/ch10/g103"
get_review_num(url, class_offset, digits)