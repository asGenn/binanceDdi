import binanceFetchData as bF
import asyncio
import pandas as pd


# Excel dosyasını oku
df = pd.read_excel('excelFiles/newsData2.xlsx')

# "new_tag" sütununda 0 değerine sahip satırları sil
df = df[df['new_tag'] != 0]
print(len(df))

# Yeni DataFrame'i Excel dosyasına yaz
df.to_excel('excelFiles/newsData2.xlsx', index=False)
