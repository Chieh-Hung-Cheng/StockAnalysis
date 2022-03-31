import os
import csv
import pandas
from datetime import datetime
import pandas as pd

base_pth = os.path.dirname(__file__)
data_pth = os.path.join(base_pth, 'data')
raw_pth = os.path.join(data_pth, 'bda2022_dataset')


def csv_to_list(doc_pth):
    with open(doc_pth, newline='', encoding='utf-8') as f:
        lst = list(csv.reader(f))
        return lst


def csv_to_df(doc_path):
    df = pandas.read_csv(doc_path, error_bad_lines=False)
    return df


def get_infos(source='news', years=('2021', '2020', '2019'), ret_header=True):
    years = sorted(years)
    ret_lst = []
    ret_header = []
    header_exist = False
    for year in years:
        if not header_exist:
            ret_header = csv_to_list(os.path.join(raw_pth, '{}_{}.csv'.format(source, year)))[0:1]
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
        header = tmp[0:1]
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


def doc_test():
    info_header, info = get_infos(years=['2021'], source='news')
    stock_header, stock = get_stocks(years=['2021'])
    y  = ['2020/1/31', '2020/1/26', '2020/12/3', '2020/2/1','2015/5/25']
    ans = []
    for i in y:
        ans.append(datetime.strptime(i, '%Y/%m/%d'))
    ans.sort()
    print(ans[1]-ans[0])
    pass


if __name__ == '__main__':
    doc_test()
