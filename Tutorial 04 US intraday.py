import pandas
import io
import requests
import datetime
import os
import time

def dataframeFromUrl(url):
	dataString = requests.get(url).content
	parsedResult = pandas.read_csv(io.StringIO(dataString.decode('utf-8')), index_col=0)
	return parsedResult

def stockPriceIntraday(ticker, folder):
	# Step 1. Get data online
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&outputsize=full&apikey=O2JFB4YQNZLGC16O&datatype=csv'.format(ticker=ticker)
	intraday = dataframeFromUrl(url)

	# Step 2. Append if history exists
	file = folder+'/'+ticker+'.csv'
	if os.path.exists(file):
		history = pandas.read_csv(file, index_col=0)
		intraday.append(history)

	# Step 3. Inverse based on index, inplace=true表示时间按顺序排列
	intraday.sort_index(inplace=True)

	# Step 4. save
	intraday.to_csv(file)
	print ('Intraday for ['+ticker+'] got.')



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

# Step 3. Get stock price (intraday)
for i, ticker in enumerate(tickers):
	try:
		print ('Intraday', i, '/', len(tickers))
		stockPriceIntraday(ticker, folder='../02. Data/04. IntradayUS')
		time.sleep(2)
	except:
		pass
print ('intraday for all stocks got.')