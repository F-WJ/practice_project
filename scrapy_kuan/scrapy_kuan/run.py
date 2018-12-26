__author__  =  'FWJ' 
__time__  =  '2018-12-26 17:01:03' 

'''
调试模式
'''
from scrapy import cmdline


name = 'kuan'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())