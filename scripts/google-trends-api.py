from pytrends.request import TrendReq


pytrends = TrendReq()

keywords = ["cloud computing", "stream processing", "AWS"]
pytrends.build_payload(keywords, cat=0, timeframe='now 1-H', geo='', gprop='')

data = pytrends.interest_over_time()
print(data.head())