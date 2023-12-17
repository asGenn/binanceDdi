class binanceData:

    def __init__(self,url,title,content,symbols,indexPrice,date):
        self.url = url
        self.title = title
        self.content = content
        self.symbols = symbols
        self.indexPrice = indexPrice
        self.date = date
    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "symbols": self.symbols,
            "indexPrice": self.indexPrice,
            "date": self.date
        }
        

    def __str__(self):
        return f"URL: {self.url}\nTitle: {self.title}\nContent: {self.content}\nSymbols: {self.symbols}\nIndexPrice: {self.indexPrice}\nDate: {self.date}\n"      

