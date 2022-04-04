import doc_utils
from datetime import datetime
from tqdm import tqdm
from collections import Counter
import phrase
import numpy as np
import other_utils


class Selector:
    def __init__(self, stocks=('Y2800 金融類',), sources=('news', 'forum'), years=('2021',), all_stock_tf=False):
        # Argument input
        self.stocks = stocks
        self.sources = sources
        self.years = years

        # Read data from CSV
        self.stocks_header, self.stocks_lst = doc_utils.get_stocks(years=self.years)
        if all_stock_tf:
            self.stocks = set(i[0] for i in self.stocks_lst)

        if 'news' in sources:
            self.news_header, self.news_lst = doc_utils.get_infos(source='news', years=self.years)
        if 'bbs' in sources:
            self.bbs_header, self.bbs_lst = doc_utils.get_bbs(years=self.years)
        if 'forum' in sources:
            self.forum_header, self.forum_lst = doc_utils.get_infos(source='forum', years=self.years)

        # Initiate interested dates
        self.up_dates = []
        self.down_dates = []

        # Initiate indexes for news, forums
        self.up_news_idxes = []
        self.down_news_idxes = []
        self.up_forum_idxes = []
        self.down_forum_idxes = []
        self.up_bbs_idxes = []
        self.down_bbs_idxes = []

        # Generate trend for specified stocks
        self.stock_trend_dict = {}
        self.gen_trends_for_stocks()

    def gen_trend_for_single_stock(self, stock_name):
        date_price_lst = []
        # Find all entries for that stock
        for stock in self.stocks_lst:
            if stock[0] == stock_name:
                date_price_lst.append(stock)

        date_price_lst = np.asarray(date_price_lst)

        minuend = date_price_lst[1:, 5].astype(float)
        subtra = date_price_lst[0:len(date_price_lst) - 1, 5].astype(float)
        amp_minus1_ratio = (minuend - subtra) / subtra
        avg_amp_ratio = np.average(np.absolute(amp_minus1_ratio))
        # amp = (date_price_lst[:, 5].astype(float) - date_price_lst[:, 2].astype(float))
        # amp_ratio = amp / date_price_lst[:, 2].astype(float)
        # avg_amp_ratio = np.average(amp_ratio)

        quantity = date_price_lst[:, 6].astype(float)
        outstanding = date_price_lst[:, 9].astype(float)
        quan_ratio = quantity / outstanding
        avg_quan_ratio = np.average(quan_ratio)

        up_lst = []
        down_lst = []

        def quan_price(sf, width=1):
            for i in range(1, len(date_price_lst) - width):
                # Omitting index 0 (amplitude with len-1)
                threshold = 0.00
                date = date_price_lst[i][1]

                if amp_minus1_ratio[i] > avg_amp_ratio and quan_ratio[i] > avg_quan_ratio:
                    if float(date_price_lst[i + width][5]) > (1 + threshold) * float(date_price_lst[i][5]):
                        up_lst.append(date)
                        if date not in sf.up_dates: sf.up_dates.append(date)
                if amp_minus1_ratio[i] < -1 * avg_amp_ratio and quan_ratio[i] < avg_quan_ratio:
                    if float(date_price_lst[i + width][5]) < (1 - threshold) * float(date_price_lst[i][5]):
                        down_lst.append(date)
                        if date not in sf.down_dates: sf.down_dates.append(date)

        def successive(sf, width=5):
            for i in range(len(date_price_lst) - width):
                up = True
                down = True
                prev = 0
                for j in range(width):
                    if j == 0:
                        prev = float(date_price_lst[i + j][5])
                    else:
                        now = float(date_price_lst[i + j][5])
                        if now > prev:
                            down = False
                        elif now < prev:
                            up = False
                        else:
                            up = False
                            down = False
                        prev = now
                # Append passing date to list
                threshold = 0.00
                if up and float(date_price_lst[i + width][5]) > (1 + threshold) * float(date_price_lst[i][5]):
                    up_lst.append(date_price_lst[i][1])
                elif down and float(date_price_lst[i + width][5]) < (1 - threshold) * float(date_price_lst[i][5]):
                    down_lst.append(date_price_lst[i][1])
            # return up_lst, down_lst

        # quan_price()
        quan_price(self)
        # Generate trends using terminate price
        self.stock_trend_dict[stock_name] = {'UPs': up_lst, 'DOWNs': down_lst}

    def gen_trends_for_stocks(self):
        # generate trend for specified stocks
        for stock in tqdm(self.stocks):
            self.gen_trend_for_single_stock(stock)

    def gen_info_idxes_on_trend(self, ret_typ='idx'):
        time_idx = 4  # self.news_header.index('post_time')
        for stock_name, trends in self.stock_trend_dict.items():
            # Each Stock
            for sc in self.sources:
                info_lst = []
                if sc == 'news':
                    info_lst = self.news_lst
                elif sc == 'forum':
                    info_lst = self.forum_lst
                elif sc == 'bbs':
                    info_lst = self.bbs_lst

                up_idxes = []
                down_idxes = []

                for idx, line in enumerate(tqdm(info_lst)):
                    info_time = datetime.strptime(line[time_idx], '%Y-%m-%d %H:%M:%S')
                    for up_day in trends['UPs']:
                        trend_date = datetime.strptime(up_day, '%Y/%m/%d')
                        if info_time < trend_date: break
                        if (info_time - trend_date).days == 0:
                            up_idxes.append(idx)
                    for down_day in trends['DOWNs']:
                        trend_date = datetime.strptime(down_day, '%Y/%m/%d')
                        if info_time < trend_date: break
                        if (info_time - trend_date).days == 0:
                            down_idxes.append(idx)

                # WRONG HERE
                if sc == 'news':
                    self.up_news_idxes = up_idxes
                    self.down_news_idxes = down_idxes
                elif sc == 'forum':
                    self.up_forum_idxes = up_idxes
                    self.down_forum_idxes = down_idxes
                elif sc == 'bbs':
                    self.up_bbs_idxes = up_idxes
                    self.down_bbs_idxes = down_idxes

    def gen_freqs(self, save=False):
        tf_up_ctr = Counter()
        df_up_ctr = Counter()
        tf_down_ctr = Counter()
        df_down_ctr = Counter()
        # News
        title_idx = 5  # self.news_header.index('title')
        content_idx = 7  # self.news_header.index('content')

        info_lst = None
        up_idxes_lst = None
        down_idxes_lst = None
        for sc in self.sources:
            if sc == 'news':
                info_lst = self.news_lst
                up_idxes_lst = self.up_news_idxes
                down_idxes_lst = self.down_news_idxes
            elif sc == 'forum':
                info_lst = self.forum_lst
                up_idxes_lst = self.up_forum_idxes
                down_idxes_lst = self.down_forum_idxes
            elif sc == 'bbs':
                info_lst = self.bbs_lst
                up_idxes_lst = self.up_bbs_idxes
                self.down_bbs_idxes = self.down_bbs_idxes

            for idx in tqdm(up_idxes_lst):
                line = info_lst[idx]
                content = line[title_idx] + line[content_idx]
                slices = self.split_sentence_to_phrase(content)
                tf_up_ctr += Counter(slices)
                df_up_ctr += Counter(set(slices))
            for idx in tqdm(self.down_news_idxes):
                line = self.news_lst[idx]
                content = line[title_idx] + line[content_idx]
                slices = self.split_sentence_to_phrase(content)
                tf_down_ctr += Counter(slices)
                df_down_ctr += Counter(set(slices))

        phrase_lst = []
        N_up = 0
        N_down = 0
        if 'news' in self.sources:
            N_up += len(self.up_news_idxes)
            N_down += len(self.down_news_idxes)
        if 'forum' in self.sources:
            N_up += len(self.up_forum_idxes)
            N_down += len(self.down_forum_idxes)
        if 'bbs' in self.sources:
            N_up += len(self.up_bbs_idxes)
            N_down += len(self.down_bbs_idxes)
        for name, times in (df_up_ctr + df_down_ctr).most_common():
            phrase_lst.append(phrase.Phrase(name=name,
                                            tf_up=tf_up_ctr[name] if name in tf_up_ctr else 0,
                                            df_up=df_up_ctr[name] if name in df_up_ctr else 0,
                                            tf_down=tf_down_ctr[name] if name in tf_down_ctr else 0,
                                            df_down=df_down_ctr[name] if name in df_down_ctr else 0,
                                            N_up=N_up,
                                            N_down=N_down))
        if save: doc_utils.phraselst_to_json(phrase_lst)

    def split_sentence_to_phrase(self, sentence):
        import monpa
        from monpa import utils
        short_sentences = utils.short_sentence(sentence)
        slices = []
        if monpa.use_gpu:
            result_cut_batch = monpa.cut_batch(short_sentences)
            for i in result_cut_batch:
                slices += i
        else:
            for elm in short_sentences:
                slices += monpa.cut(elm)
        return [i.strip(' -') for i in slices if len(i.strip(' -')) >= 2 and not other_utils.has_digit(i.strip())]



def selector_test():
    lbr = Selector(sources=('bbs',), years=('2021',))
    lbr.gen_info_idxes_on_trend()
    lbr.gen_freqs(save=False)
    pass


if __name__ == '__main__':
    selector_test()
