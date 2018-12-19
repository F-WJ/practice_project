__author__  =  'FWJ' 
__time__  =  '2018-12-17 17:33:24' 

import pandas as pd

df = pd.DataFrame({'col1': ['one', 'one', 'two', 'two', 'two', 'three', 'four'], 'col2': [1, 2, 1, 2, 1, 1, 1],
                   'col3':['AA','BB','CC','DD','EE','FF','GG']},index=['a', 'a', 'b', 'c', 'b', 'a','c'])

test = df.duplicated()

print(df)
print(test)