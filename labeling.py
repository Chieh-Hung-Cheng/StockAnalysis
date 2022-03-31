import doc_utils
from datetime import datetime
from tqdm import tqdm
from collections import Counter
import phrase


class Labeler:
    def __init__(self, stocks=('0050 元大台灣50',), sources=('news',), years=('2021',), all_stock_tf=False):
        self.stocks = stocks
        self.sources = sources
        self.years = years

        self.stocks_header, self.stocks_lst = doc_utils.get_stocks(years=self.years)
        if all_stock_tf:
            self.stocks = set(i[0] for i in self.stocks_lst)

        if 'news' in sources:
            self.news_header, self.news_lst = doc_utils.get_infos(source='news', years=self.years)
        if 'bbs' in sources:
            self.bbs_header, self.bbs_lst = doc_utils.get_infos(source='bbs', years=self.years)
        if 'forum' in sources:
            self.forum_header, self.forum_lst = doc_utils.get_infos(source='forum', years=self.years)

        self.stock_trend_dict = {}
        self.gen_trends_4_stocks()

    def gen_trend_4_stock(self, stock_name, width=5):
        date_price_lst = []
        # Find all entries for that stock
        for stock in self.stocks_lst:
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
        self.stock_trend_dict[stock_name] = {'UPs': up_lst, 'DOWNs': down_lst}

    def gen_trends_4_stocks(self):
        # generate trend for specified stocks
        for stock in tqdm(self.stocks):
            self.gen_trend_4_stock(stock)

    def gen_news_on_trend(self, ret_typ='idx'):
        time_idx = self.news_header.index('post_time')
        up_news = []
        self.up_news_idxes = []
        down_news = []
        self.down_news_idxes = []
        for key, value in self.stock_trend_dict.items():
            # Each Stock
            stock_name = key
            trend = value
            for idx, line in enumerate(tqdm(self.news_lst)):
                info_time = datetime.strptime(line[time_idx], '%Y-%m-%d %H:%M:%S')
                for up_day in trend['UPs']:
                    trend_date = datetime.strptime(up_day, '%Y/%m/%d')
                    if info_time < trend_date: break
                    if (info_time - trend_date).days == 0:
                        up_news.append(line)
                        self.up_news_idxes.append(idx)
                for down_day in trend['DOWNs']:
                    trend_date = datetime.strptime(down_day, '%Y/%m/%d')
                    if info_time < trend_date: break
                    if (info_time - trend_date).days == 0:
                        down_news.append(line)
                        self.down_news_idxes.append(idx)
        if ret_typ == 'idx':
            return self.up_news_idxes, self.down_news_idxes
        else:
            return up_news, down_news

    def gen_freqs(self):
        tf_up_ctr = Counter()
        df_up_ctr = Counter()
        tf_down_ctr = Counter()
        df_down_ctr = Counter()
        title_idx = self.news_header.index('title')
        content_idx = self.news_header.index('content')

        for idx in tqdm(self.up_news_idxes):
            line = self.news_lst[idx]
            content = line[title_idx] + line[content_idx]
            slices = phrase.split_sentence_to_phrase(content)
            tf_up_ctr += Counter(slices)
            df_up_ctr += Counter(set(slices))

        for idx in tqdm(self.down_news_idxes):
            line = self.news_lst[idx]
            content = line[title_idx] + line[content_idx]
            slices = phrase.split_sentence_to_phrase(content)
            tf_down_ctr += Counter(slices)
            df_down_ctr += Counter(set(slices))

        '''for idx, line in enumerate(tqdm(self.news_lst)):
            content = line[title_idx] + line[content_idx]
            slices = phrase.split_sentence_to_phrase(content)
            new_tf = Counter(slices)
            new_df = Counter(set(slices))
            tf_all_ctr += new_tf
            df_all_ctr += new_df
            if idx in self.up_news_idxes:
                tf_up_ctr += new_tf
                df_up_ctr += new_df
            if idx in self.down_news_idxes:
                tf_down_ctr += new_tf
                df_down_ctr += new_df'''
        phrase_lst = []
        for name, times in (df_up_ctr + df_down_ctr).most_common():
            phrase_lst.append(phrase.Phrase(name=name,
                                            tf_up=tf_up_ctr[name] if name in tf_up_ctr else 0,
                                            df_up=df_up_ctr[name] if name in df_up_ctr else 0,
                                            tf_down=tf_down_ctr[name] if name in tf_down_ctr else 0,
                                            df_down=df_down_ctr[name] if name in df_down_ctr else 0,
                                            N_up=len(self.up_news_idxes),
                                            N_down=len(self.down_news_idxes)))
        doc_utils.phraselst_2_json(phrase_lst)


def labeling_test():
    lbr = Labeler()
    up_news_idxes, down_news_idxes = lbr.gen_news_on_trend()
    lbr.gen_freqs()
    pass


if __name__ == '__main__':
    labeling_test()
