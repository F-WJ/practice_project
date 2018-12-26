# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()   # app名字
    volume = scrapy.Field()  # app大小
    download = scrapy.Field()  # 下载数量
    follow = scrapy.Field()   # 关注量
    comment = scrapy.Field()  # 评论数
    tags = scrapy.Field()  # 标签
    score = scrapy.Field()  # 点评
    num_score = scrapy.Field()  # 评分数量
    
