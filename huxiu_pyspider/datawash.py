__author__  =  'FWJ' 
__time__  =  '2018-12-17 11:41:23' 
import pymongo
import  pandas as pd


client = pymongo.MongoClient(host='localhost', port=27017)
db = client['Huxiu']
collection = db['huxiu_news']
data = pd.DataFrame(list(collection.find()))

# 导出数据
# data.to_csv("original.csv")
# print(data.shape)
# print(data.info)
# print(data.head())


# 删除_id列
data.drop(['_id'], axis=1, inplace=True) 
# 替换特殊字符（通过正则表达式进行替换回车、换行、空白符号）
data['name'].replace('©', '', inplace=True, regex=True)
data['abstract'].replace('\r|\n|\\s|转推', '', inplace=True, regex=True)
# data['abstract'].replace('“', '', inplace=True, regex=True)
# 字符改为数值
data = data.apply(pd.to_numeric, errors='ignore')
# 更改日期格式
data['write_time'] = data['write_time'].replace('.*前', '2018-12-09', regex=True)
data['write_time'] = pd.to_datetime(data['write_time'])
# 文章标题长度
data['title_length'] = data['title'].apply(len)
# 年份列
data['year'] = data['write_time'].dt.year
# 查看类型
print(data.dtypes)
# 判断是否有重复值
print(any(data.duplicated()))
# 查看重复值数量
data_duplicated = data.duplicated().value_counts()
# 删除重复值
data = data.drop_duplicates(keep='first')
# 重新设置index
data = data.reset_index(drop=True)
print(data.dtypes)

data.to_csv("datawash.csv")
print(data.shape)
# print(data.info)
# print(data.head())





