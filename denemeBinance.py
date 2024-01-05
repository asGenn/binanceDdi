import binanceFetchData as bF
import asyncio
import pandas as pd
import matplotlib.pyplot as plt


# Excel dosyasını oku
df = pd.read_excel('excelFiles/newsData2.xlsx')

# "new_tag" sütununda 0 değerine sahip satırları sil
df = df[df['new_tag'] != 0]
print(df.new_tag.value_counts())
df.new_tag.value_counts().plot(kind='bar',
                               x='Kategoriler',
                               y='Veri Miktarı',
                               color='green')
plt.title('Veri Seti')
plt.show()
