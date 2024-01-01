import pandas as pd
"""
dosya1 = pd.read_excel('veriler3.xlsx')
dosya2 = pd.read_excel('veriler4.xlsx')


mergedFile = pd.concat([dosya1,dosya2],ignore_index=False)
mergedFile.to_excel('newsData.xlsx',index=False)
"""

df = pd.read_excel('excelFiles/newsData2.xlsx')
df["symbols"]

print(df["symbols"][0])
print(list(df["symbols"][0]))
string_ifade = df["symbols"][0]

# İlk olarak string ifadeyi temizleyerek sadece öğeleri içeren bir string elde edelim
temizlenmis_ifade = string_ifade.replace(
    "[", "").replace("]", "").replace("'", "")

# Sonra, virgülle ayrılmış öğelerden oluşan bir liste elde edelim
liste = temizlenmis_ifade.split(", ")

print(liste)
