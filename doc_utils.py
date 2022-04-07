import os
import csv

import numpy as np
from datetime import datetime
import pandas as pd
import json
import phrase
from collections import Counter

# import openpyxl

base_pth = os.path.dirname(__file__)
data_pth = os.path.join(base_pth, 'data')
raw_pth = os.path.join(data_pth, 'bda2022_dataset')
pros_pth = os.path.join(data_pth, 'pros')


def csv_to_df(path):
    return pd.read_csv(path)


def df_to_csv(df, path):
    df.to_csv(path, encoding='utf_8_sig')


def get_news_df():
    news2019 = csv_to_df(os.path.join(raw_pth, 'bda2022_mid_news_2019.csv'))
    news2020 = csv_to_df(os.path.join(raw_pth, 'bda2022_mid_news_2020.csv'))
    news2021 = csv_to_df(os.path.join(raw_pth, 'bda2022_mid_news_2021.csv'))
    news = pd.concat([news2019, news2020, news2021])
    return news


def csv_to_list(doc_pth):
    with open(doc_pth, 'r', newline='', encoding='utf-8') as f:
        lst = list(csv.reader(f))
        return lst


def xlsx_to_csv():
    df = pd.read_excel(os.path.join(raw_pth, 'stock_data_2019-2021.xlsx'), sheet_name=None)
    y = 0


def get_bbs(years=('2021', '2020', '2019'), ret_header=True):
    # Read news or forums
    ret_lst = []
    ret_header = []
    lst = csv_to_list(os.path.join(raw_pth, 'bda2022_mid_bbs_2019-2021.csv'))
    ret_header = lst[0]  # :1]
    bbs2019 = lst[1:20832]
    bbs2020 = lst[20832:55891]
    bbs2021 = lst[55891:]

    ret_lst = []
    if '2019' in years: ret_lst += bbs2019
    if '2020' in years: ret_lst += bbs2020
    if '2021' in years: ret_lst += bbs2021

    if ret_header:
        return ret_header, ret_lst
    else:
        return ret_lst


def get_infos(source='news', years=('2021', '2020', '2019'), ret_header=True):
    # Read news or forums
    years = sorted(years)
    ret_lst = []
    ret_header = []
    header_exist = False
    for year in years:
        if not header_exist:
            ret_header = csv_to_list(os.path.join(raw_pth, 'bda2022_mid_{}_{}.csv'.format(source, year)))[0]  # :1]
            header_exist = True
        ret_lst += csv_to_list(os.path.join(raw_pth, 'bda2022_mid_{}_{}.csv'.format(source, year)))[1:]
    if ret_header:
        return ret_header, ret_lst
    else:
        return ret_lst


def get_stocks(mkt_typ='0', years=('2021', '2020', '2019'), ret_header=True):
    # Reorder from old to new
    years = sorted(years)
    ret_lst = []
    ret_header = []
    header_exist = False
    for year in years:
        tmp = csv_to_list(os.path.join(pros_pth, 'stock_{}_{}.csv'.format(year, mkt_typ)))

        header = tmp[0]  # :1]
        tmp = tmp[1:]
        tmp.reverse()
        if not header_exist:
            ret_header = header
            # ret_lst += header
            header_exist = True
        ret_lst += tmp
    if ret_header:
        return ret_header, ret_lst
    else:
        return ret_lst


def phraselst_to_json(phraselist):
    with open(os.path.join(pros_pth, 'phraselist_{}.json'.format(datetime.now().strftime('%m%d%H%M'))), 'w') as file:
        json.dump(phraselist, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print('Save Phrase List Complete')


def json_to_phraselst(filename='phraselist.json'):
    path = os.path.join(pros_pth, filename)
    with open(path, 'r') as file:
        dictlist = json.load(file)
    ret_list = []
    for elm in dictlist:
        ret_list.append(phrase.Phrase(**elm))
    print('Load Phrase List Complete')
    return ret_list


def ctr_to_json(counter, category, frqtype='tf'):
    with open(os.path.join(pros_pth, '{}_{}.json'.format(frqtype, category), 'w')) as file:
        json.dump(counter, file)
        print('Save Counter Complete')


def json_to_ctr(category, frqtype):
    with open(os.path.join(pros_pth, '{}_{}.json'.format(frqtype, category), 'r')) as file:
        counter = Counter(json.load(file))
        print('Load Counter Complete')


def to_json(data, filename='jsonfile_{}'.format(datetime.now().strftime('%m%d%H%M'))):
    path = os.path.join(pros_pth, filename)
    with open(path, 'w') as file:
        json.dump(data, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print('Save json complete')


def doc_test():
    # info_header, info = get_infos(years=['2021'], source='forum')
    # stock_header, stock = get_stocks(years=['2021'])
    # xlsx_to_csv()
    bbs_header, bbs = get_bbs(years=('2021', '2019'))
    y = 0
    # bbs_header, bbs = get_bbs()

    pass


if __name__ == '__main__':
    doc_test()
