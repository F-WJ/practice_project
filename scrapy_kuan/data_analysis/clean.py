__author__  =  'FWJ' 
__time__  =  '2018-12-29 11:33:04' 
import pymongo
import pandas as pd

def clean_data():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['Kuan']
    collection = db['kuanapp']

    data = pd.DataFrame(list(collection.find()))
    data['score'] = data['score'].astype('float64')
    data.to_csv('ori_data.csv')
    # 去除_id列
    data = data.drop(['_id'], axis=1)

    # 处理＇万＇字同＇Ｍ＇字
    cols = ['comment', 'download', 'follow', 'num_score', 'volume']
    for col in cols:
        # col_ori = col + '_ori'
        # data[col_ori] = data[col]
        if not (col=='volume'):
            data[col] = clean_symbol1(data, col)
        else:
            data[col] = clean_symbol2(data, col)
    


    print(data.shape)
    print(data.head())
    # print('-----------------------')
    # print(data.shape)
    # print('-----------------------')
    # print(data.info())
    # print('-----------------------')
    print(data.dtypes)
    print(data.describe())
    data.to_csv('clean_data.csv')


def clean_symbol1(data, col):
    '''
    除去万字
    '''
    con = data[col].str.contains('万$')
    data.loc[con, col] = pd.to_numeric(data.loc[con, col].str.replace('万', '')) * 10000
    data[col] = pd.to_numeric(data[col])
    return data[col]
    


def clean_symbol2(data, col):
    '''
    除去字符Ｍ
    '''
    data[col] = data[col].str.replace('M$', '')
    # 体积为Ｋ的除以1024转换为Ｍ
    con = data[col].str.contains('K$')
    data.loc[con, col] = pd.to_numeric(data.loc[con, col].str.replace('K$', ''))/1024
    data[col] = pd.to_numeric(data[col])
    return data[col]



if __name__ == "__main__":
    clean_data()
