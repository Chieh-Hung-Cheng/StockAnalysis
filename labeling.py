import time

import doc_utils
from datetime import datetime
from tqdm import tqdm


def gen_stock_trend(stock_name, stocks_lst, tgt_dict, width=5):
    date_price_lst = []
    # Find all entries for that stock
    for stock in stocks_lst:
        if stock[0] == stock_name:
            date_price_lst.append(stock)
    # Generate trends using terminate price
    up_lst = []
    down_lst = []
    for i in range(len(date_price_lst) - width):
        up = True
        down = True
        for j in range(width):
            if j == 0:
                prev = date_price_lst[i + j][5]
            else:
                now = date_price_lst[i + j][5]
                if now > prev:
                    down = False
                elif now < prev:
                    up = False
                else:
                    up = False
                    down = False
                prev = now
        # Append passing date to list
        if up:
            up_lst.append(date_price_lst[i][1])
        elif down:
            down_lst.append(date_price_lst[i][1])
    tgt_dict[stock_name] = {'UPs': up_lst, 'DOWNs': down_lst}


def gen_trends_for_stocks(stocks=('0050 元大台灣50', '2330 台積電'), gen_all_stocks=False, years=('2021', '2020', '2019')):
    stock_header, stocks_lst = doc_utils.get_stocks(mkt_typ='0', years=years)
    if gen_all_stocks:
        stocks = set(i[0] for i in stocks_lst)
    # generate trend for specified stocks
    tgt_dict = {}
    for stock in tqdm(stocks):
        gen_stock_trend(stock, stocks_lst, tgt_dict)
    return tgt_dict


def labeling_test():
    stock_trend_dict = gen_trends_for_stocks(stocks=['0050 元大台灣50'], years=['2021'])
    header, news = doc_utils.get_infos(source='news', years=['2021'])

    time_idx = header.index('post_time')
    up_news = []
    down_news = []
    for key, value in stock_trend_dict.items():
        # Each Stock
        stock_name = key
        trend = value
        for line in tqdm(news):
            info_time = datetime.strptime(line[time_idx], '%Y-%m-%d %H:%M:%S')
            for up_day in trend['UPs']:
                trend_date = datetime.strptime(up_day, '%Y/%m/%d')
                if info_time < trend_date: break
                if (info_time - trend_date).days == 0:
                    up_news.append(line)
            for down_day in trend['DOWNs']:
                trend_date = datetime.strptime(down_day, '%Y/%m/%d')
                if info_time < trend_date: break
                if (info_time - trend_date).days == 0:
                    down_news.append(line)

        pass


if __name__ == '__main__':
    labeling_test()
