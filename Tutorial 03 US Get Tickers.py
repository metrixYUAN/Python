import pandas
import io
import requests
import datetime

# Step 1.Get tickers list online
url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
# 下载网页字符流，但其为字符流无法解读
dataString = requests.get(url).content
# 用pandas解读， 用IO转码成utf-8格式
tickersRawData = pandas.read_csv(io.StringIO(dataString.decode('utf-8')))
# 获得tickers
tickers = tickersRawData['Symbol'].tolist()

#Step 2. Save the tikcer list to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../02. Data/02. TickerListUS/TickerList'+dateToday+'.csv'
tickersRawData.to_csv(file, index=False)
print ('Tickers saved')