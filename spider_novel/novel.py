__author__  =  'FWJ' 
__time__  =  '2018-11-18 15:18:25' 

import requests
from bs4 import BeautifulSoup
import re
import multiprocessing


def get_html(url):
    '''
    获取网页内容
    '''
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=30)
        a = r.raise_for_status
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print('错误: ', e)


def get_content(url):
    '''
    获取全网所有小说链接
    '''
    url_list = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    category_list = soup.find_all('div', class_='index_toplist mright mbottom')
    # 历史小说和完本是一类
    history_list = soup.find_all('div', class_='index_toplist mbottom')

    for cate in category_list:
        name = cate.find('div', class_='toptab').span.text
        with open('novel_list.csv', 'a+') as f:
            f.write('\n小说种类：{} \n'.format(name))

        book_list = cate.find('div', class_='topbooks').find_all('li')


        for book in book_list:
            link = 'http://www.qu.la' + book.a['href']
            title = book.a['title']
            url_list.append(link)

            with open('novel_list.csv', 'a') as f:
                f.write('小说名：{} \t 小说地址：{} \n'.format(title, link))


    for cate in history_list:
        name = cate.find('div', class_='toptab').span.text
        with open('novel_list.csv', 'a') as f:
            f.write('\n小说种类: {} \n'.format(name))

        book_list = cate.find('div', class_='topbooks').find_all('li')

        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)

            with open('novel_list.csv', 'a') as f:
                f.write('小说名: {} \t 小说地址: {} \n'.format(title, link))

    return url_list


def get_txt_url(url):
    '''
    获取单本小说所有章节链接
    '''
    url_lists = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    dt = soup.find_all('dt')[1].text
    txt_name = re.search('《(.+)》', dt).group(1)
    list_a = soup.find_all('dd')


    with open('./小说/{}.txt'.format(txt_name), 'a+') as f:
        f.write('小说标题: {} \n'.format(txt_name))

    for url in list_a:
        url_list = 'http://www.qu.la/' + url.a['href']
        re_url = re.compile('.*?book.*?')
        if re_url.match(url_list) != None:
            url_lists.append(url_list)

    return url_lists, txt_name


def get_one_txt(url, txt_name):
    '''
    获取单页文章内容并保存到本地
    '''
    html = get_html(url).replace('<br/>', '\n').replace('chaptererror();', '')
    soup = BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text
        title = soup.find('h1').text

        with open('./小说/{}.txt'.format(txt_name), 'a') as f:
            f.write(title + '\n\n')
            f.write(txt)
            print('当前小说: {}当前章节{}已经下载完毕'.format(txt_name, title))
    except:
        print('当前小说: {}当前章节{}下载失败'.format(txt_name, title))



def get_all_txt(url_list):
    # 爬取所有章节链接
    page_list, txt_name = get_txt_url(url_list)
    # 爬取所有章节内容
    for page in page_list:
        get_one_txt(page, txt_name)


def main():
    '''
    主函数
    '''
    base_url = 'http://www.qu.la/paihangbang/'
    url_lists = get_content(base_url)
    # 去除重复小说
    url_lists = list(set(url_lists))
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for url_list in url_lists:
        pool.apply_async(get_all_txt, (url_list, ))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()