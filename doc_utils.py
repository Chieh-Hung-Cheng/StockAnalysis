import os
import csv
import pandas
from datetime import datetime
import pandas as pd
import json
import phrase

base_pth = os.path.dirname(__file__)
data_pth = os.path.join(base_pth, 'data')
raw_pth = os.path.join(data_pth, 'bda2022_dataset')
pros_pth = os.path.join(data_pth, 'pros')


def csv_to_list(doc_pth):
    with open(doc_pth, 'r', newline='', encoding='utf-8') as f:
        lst = list(csv.reader(f))
        return lst


def get_infos(source='news', years=('2021', '2020', '2019'), ret_header=True):
    years = sorted(years)
    ret_lst = []
    ret_header = []
    header_exist = False
    for year in years:
        if not header_exist:
            ret_header = csv_to_list(os.path.join(raw_pth, '{}_{}.csv'.format(source, year)))[0]  # :1]
            header_exist = True
        ret_lst += csv_to_list(os.path.join(raw_pth, '{}_{}.csv'.format(source, year)))[1:]
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
        tmp = csv_to_list(os.path.join(raw_pth, 'stock_{}_{}.csv'.format(year, mkt_typ)))
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


def phraselst_2_json(phraselist):
    with open(os.path.join(pros_pth, 'phraselist.json'), 'w') as file:
        json.dump(phraselist, file, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print('Save Phrase List Complete')


def json_2_phraselst(path=os.path.join(pros_pth, 'phraselist.json')):
    with open(path, 'r') as file:
        dictlist = json.load(file)
    ret_list = []
    for elm in dictlist:
        ret_list.append(phrase.Phrase(**elm))
    print('Load Phrase List Complete')
    return ret_list


def doc_test():
    # info_header, info = get_infos(years=['2021'], source='news')
    # stock_header, stock = get_stocks(years=['2021'])
    stock = datetime.strptime('2015-05-19 00:00:00', '%Y-%m-%d %H:%M:%S')
    info = datetime.strptime('2015-05-19 09:30:51', '%Y-%m-%d %H:%M:%S')
    pass


if __name__ == '__main__':
    doc_test()
