__author__  =  'FWJ' 
__time__  =  '2018-10-31 14:36:54' 
import tushare as ts
import config

# 设置token
ts.set_token(config.mytoken)
# 初始化pro接口
pro = ts.pro_api()
# 数据调取
df = pro.bo_daily(date='20181030')
print(df)