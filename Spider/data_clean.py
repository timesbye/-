import pandas as pd

df = pd.read_csv('data.csv')

df['评分'] = df['评分'].astype(str)
df['评分'] = df['评分'].str.replace()
df['可住'] = df['可住'].str.replace('宜住','')
df['价格'] = df['价格'].str.replace('￥','')
df['评分'] = df['评分'].str.replace('\r\n','')

df = df.astype(str)
df = df.applymap(lambda x:x.replace(',',''))

df.dropna(inplace = True)
df.to_csv('data_clean',index = True)