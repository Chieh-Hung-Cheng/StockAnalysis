import time

import doc_utils
import datetime
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
    tgt_dict[stock_name]= {'UPs': up_lst, 'DOWNs': down_lst}


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
    ret_dict = gen_trends_for_stocks(gen_all_stocks=True)
    # gen_stock_trend('0050 元大台灣50', stocks_lst, tgtdict)
    pass


if __name__ == '__main__':
    labeling_test()
