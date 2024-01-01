import pandas as pd
import convertClock as cc
df = pd.read_excel('excelFiles/newsData.xlsx')


def convertDate(row):
    saat = cc.converToDateTime(row['date'])
    return saat


df['date'] = df.apply(lambda row: convertDate(row), axis=1)
df.to_excel('excelFiles/newsData2.xlsx', index=False)
