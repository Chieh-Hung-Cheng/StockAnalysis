import os
import csv
import pandas
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


def get_news():
    postfixes = ['2019', '2020', '2021']
    # if typ == 'lst':
    ret_lst = []
    for postfix in postfixes:
        ret_lst += csv_to_list(os.path.join(raw_pth, 'news_{}.csv'.format(postfix)))
    return ret_lst
    '''elif typ == 'df':
        ret_df = pandas.DataFrame()
        for postfix in postfixes:
            pandas.concat([ret_df, csv_to_df(os.path.join(raw_pth, 'news_{}.csv'.format(postfix)))])
        return ret_df'''


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
    '''
    xls = pd.ExcelFile(os.path.join(raw_pth, 'stock_data_2019-2021.xlsx'))
    markets = ['上市']  # , '上櫃']
    years = ['2019', '2020', '2021']
    df_lst = []
    for market in markets:
        for year in years:
            df_lst.append(pd.read_excel(xls, '{}{}'.format(market,year)))
        return pd.concat(df_lst, axis=0)


    years = ['2019'] #, '2020', '2021']
    sheetname = '{}{}'.format(markets[0], years[0])

    dfs_lst = []
    for market in markets:
        df_lst = []
        for year in years:
            
            df_lst.append(pd.read_excel(os.path.join(raw_pth, 'stock_data_2019-2021.xlsx'), sheet_name=sheetname))
        dfs_lst.append(pd.concat(df_lst, axis=0))

    df = pd.read_excel(os.path.join(raw_pth, 'stock_data_2019-2021.xlsx'), sheet_name=sheetname)
    return df'''


def doc_test():
    news_lst = get_news()
    forum_lst = get_forums()
    bbs_lst = get_bbs()
    stock_lst = get_stock_data()
    pass


if __name__ == '__main__':
    doc_test()
