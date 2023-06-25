import requests
from apikey import API_KEY, bot_token1, bot_chatID1

api_key = API_KEY
news_api = "73991c7f93bc41b38ed939ce55f56617"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_params = {
    "symbol": STOCK,
    "apikey": api_key,
    "function" : "TIME_SERIES_DAILY_ADJUSTED"
}
news_params = {
    "qInTitle" : COMPANY_NAME,
    "apiKey" : news_api
}

url = "https://www.alphavantage.co/query"
news_url = "https://newsapi.org/v2/everything"

def telegram_bot_sendtext(bot_message):
    bot_token = bot_token1
    bot_chatID = bot_chatID1
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    text_response = requests.get(send_text)
    return text_response.json()


response = requests.get(url,params=stock_params)
data = response.json()
daily_data = data['Time Series (Daily)']
data_list = [value for (key,value) in daily_data.items()]
# day = dt.datetime.now().day

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data['4. close'])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

# print(data_list)
# print(yesterday_closing_price)
# print(day_before_yesterday_closing_price)
difference = (day_before_yesterday_closing_price-yesterday_closing_price)
if difference>0:
    sign = "🔻"
else:
    sign = "🔺"
diff_percent = abs(difference)*100/yesterday_closing_price
if diff_percent >= 1:
    news_response = requests.get(news_url, params=news_params)
    three_article_list = news_response.json()["articles"][:3]
    telegram_bot_sendtext(f"hi ishita, {sign + str(diff_percent)}% change observed")
    for item in three_article_list:
        title = "Headline: " + item['title']
        brief = "\n Brief: " + item['content']
        # print(title+brief)
        telegram_bot_sendtext(title+brief)



