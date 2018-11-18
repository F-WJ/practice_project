import requests
import json
from pyquery import PyQuery as pq
import os
import urllib


proxies = {
    'http': 'hhtp://127.0.0.1:12333',
    'https': 'https://127.0.0.1:12333'
}

def ins_url():
    '''
    爬取图片
    '''


    insurl = 'https://www.instagram.com/1004yul_i/'
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}

    # print(requests.get('http://www.icanhazip.com/').text)   # 查询当前ip
    inscontent = requests.get(insurl, proxies=proxies, headers=headers, timeout=24)
    
    # 捉取关键信息
    imageurls = []
    number = 1
    doc = pq(inscontent.text)
    items = doc('script[type="text/javascript"]').items()

    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            for edge in edges:
                imageurl = edge['node']['display_url']
                print(imageurl)
                save_img(imageurl, number)
                imageurls.append(imageurl)
                number = number + 1

    
def save_img(imageurl, number, file_path='ins'):
    '''
    下载
    '''
    # urlretrieve方法
    # urlretrieve(imageurl, "{}.jpg".format(number))
    try:
        if not os.path.exists(file_path):
            print('文件夹不存在', file_path, '正在自动创建')
            os.makedirs(file_path)
        
        file_suffix = os.path.splitext(imageurl)[1]
        filename = '{}{}{}{}'.format(file_path, os.sep, number, file_suffix)
        # urllib.request.urlretrieve(imageurl, filename=filename) 
        # 墙的问题，还是用requests
        ir = requests.get(imageurl, proxies=proxies)
        if ir.status_code == 200:
            open(filename, 'wb').write(ir.content)
                
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误：', e)

        

    
    


ins_url()

