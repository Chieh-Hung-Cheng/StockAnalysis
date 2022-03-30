import os
import csv
import pandas

base_pth = os.path.dirname(__file__)
data_pth = os.path.join(base_pth, 'data')
raw_pth = os.path.join(data_pth, 'bda2022_dataset')


def csv_to_list(doc_pth):
    with open(doc_pth, newline='', encoding='utf-8') as f:
        lst = list(csv.reader(f))
        return lst


def csv_to_df(doc_path):
    with open(doc_path, newline='', encoding='utf-8') as f:
        df = pandas.read_csv()
        return df


def get_news(typ):
    postfixes = ['2019', '2020', '2021']
    if typ == 'lst':
        ret_lst = []
        for postfix in postfixes:
            ret_lst += csv_to_list(os.path.join(raw_pth, 'news_{}.csv'.format(postfix)))
        return ret_lst
    elif typ == 'df':
        for postfix in postfixes:
            csv_to_df(os.path.join(raw_pth, 'news_{}.csv'.format(postfix)))


def get_forums():
    postfixes = ['2019-2020', '2021']
    ret_lst = []
    for postfix in postfixes:
        ret_lst += csv_to_list(os.path.join(raw_pth, 'forum_{}.csv'.format(postfix)))
    return ret_lst


def get_bbs():
    postfixes = ['2019-2020', '2021']
    ret_lst = []
    for postfix in postfixes:
        ret_lst += csv_to_list(os.path.join(raw_pth, 'bbs_{}.csv'.format(postfix)))
    return ret_lst


def get_stock_data():
    df = pandas.read_excel(os.path.join(raw_pth, 'stock_data_2019-2021.xlsx'), sheet_name='上市2021')
    return df


def doctest():
    news_lst = get_news('df')
    # forum_lst = get_forums()
    # bbs_lst = get_bbs()
    stock_lst = get_stock_data()
    pass


if __name__ == '__main__':
    doctest()
