import os
import sys
import csv




def readcsv():
    pass

def main():
    base_pth = os.path.dirname(__file__)
    raw_pth = os.path.join(base_pth, 'data/bda2022_dataset')
    with open(os.path.join(raw_pth, 'news_2021.csv'), newline='', encoding='utf-8') as f:
        lines = list(csv.reader(f))
        pass



if __name__ == '__main__':
    main()

