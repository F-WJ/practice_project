# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy_kuan.items import KuanItem
from fake_useragent import UserAgent
# from scrapy.shell import inspect_response

ua = UserAgent()
headers = {
    'User-Agent': ua.chrome,
}


class KuanSpider(scrapy.Spider):

    # 延时爬取设置
    custom_settings = {
        "DOWNLOAD_DELAY": 1,   # 默认是0
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8   # 每秒并发８次
    }

    name = 'kuan'
    allowed_domains = ['www.coolapk.com']
    start_urls = ['http://www.coolapk.com/apk/']

    def parse(self, response):
        contents = response.css('.app_left_list>a')
        for content in contents:
            url = content.css('::attr("href")').extract_first()
            url = response.urljoin(url) # 拼接，因为爬取地址是相对地址
            yield scrapy.Request(url, callback=self.parse_url, headers=headers)
        
        next_page = response.css('.pagination li:nth-child(8) a::attr(href)').extract_first()
        url = response.urljoin(next_page)
        yield scrapy.Request(url, callback=self.parse, headers=headers)
        
    
    def parse_url(self, response):
        item = KuanItem()
        item['name'] = response.css('.detail_app_title::text').extract_first()
        # print('name:' + item['name'])
        results = self.get_comment(response)
        item['volume'] = results[0]
        item['download'] = results[1]
        item['follow'] = results[2]
        item['comment'] = results[3]
        item['tags'] = self.get_tags(response)
        item['score'] = response.css('.rank_num::text').extract_first()
        num_score = response.css('.apk_rank_p1::text').extract_first()
        item['num_score'] = re.search('共(.*?)个评分', num_score).group(1)
        yield item


    def get_comment(self, response):
        messages = response.css('.apk_topba_message::text').extract_first()
        result = re.findall(r'\s+(.*?)\s+/\s+(.*?)下载\s+/\s+(.*?)人关注\s+/\s+(.*?)个评论.*?', messages)
        if result:
            results = list(result[0])
            # print(results)
            return results
        
    def get_tags(self, response):
        data = response.css('.apk_left_span2')
        tags = [item.css('::text').extract_first() for item in data]
        # print(tags)
        return tags

