from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
from collections import Counter
import doc_utils
import other_utils
import phrase
import phraselst
import pandas as pd
import os
import datetime


class Screener:
    def __init__(self, from_scratch=False):
        self.finance_related = ['彰銀', '京城銀', '台中銀', '旺旺保', '華票', '台產', '臺企銀', '高雄銀', '高雄銀甲特', '聯邦銀', '聯邦銀甲特', '遠東銀',
                                '安泰銀', '新產', '中再保', '第一保', '統一證', '三商壽', '華南金', '富邦金',
                                '富邦特', '國泰金', '國泰特', '開發金', '玉山金', '元大金', '兆豐金', '台新金', '台新戊特', '新光金', '國票金', '永豐金',
                                '中信金', '第一金', '王道銀', '上海商銀', '合庫金', '群益證', '群益期']

        self.strict_bound = ['金融', '金控']
        self.up_kwd = ['漲', '反彈', '揚', '買壓']
        self.down_kwd = ['跌', '失守', '觀望', '保守', '緩', '賣壓', '挫']
        self.mutual_forb = ['震盪', '止', '抗', '整理']

        self.up_news = None
        self.down_news = None
        self.phraselst = None

        self.news_df = doc_utils.get_news_df()
        if from_scratch:
            self.gen_filtered_news()
            self.slice_each_news()
        self.gen_vectors_each_news()

    def news_filter(self, news, kws, prohs, cstl=True, csct=True):
        def check(title, content, keywords, prohibits, cons_tl=True, cons_ct=True):
            string = ''
            if cons_tl: string += title
            if cons_ct and isinstance(content, str): string += content

            for i in keywords:
                if i in string:
                    if prohibits is not None:
                        for j in prohibits:
                            if j in string:
                                return False
                    return True
                else:
                    continue
            return False

        filtered = []
        for idx, line in tqdm(news.iterrows()):
            # string = line['title']
            # if isinstance(line['content'], str): string+= line['content']
            # if checkfinance(string): filtered.append(line)
            if check(line['title'], line['content'], kws, prohs, cons_tl=cstl, cons_ct=csct): filtered.append(line)

        if len(filtered) != 0:
            ret_news = pd.concat(filtered, axis=1)
            ret_news = ret_news.T
            return ret_news
        else:
            return None

    def gen_filtered_news(self):
        news = self.news_filter(self.news_df, self.finance_related, None)
        news.to_csv(os.path.join(doc_utils.pros_pth, 'filtered_0.csv'), encoding='utf_8_sig')
        news = self.news_filter(news, self.strict_bound, None)
        news.to_csv(os.path.join(doc_utils.pros_pth, 'filtered_1.csv'), encoding='utf_8_sig')
        self.up_news = self.news_filter(news, self.up_kwd, self.down_kwd + self.mutual_forb, csct=False)
        self.down_news = self.news_filter(news, self.down_kwd, self.up_kwd + self.mutual_forb, csct=False)
        self.up_news.to_csv(os.path.join(doc_utils.pros_pth, 'filtered_up.csv'), encoding='utf_8_sig')
        self.down_news.to_csv(os.path.join(doc_utils.pros_pth, 'filtered_down.csv'), encoding='utf_8_sig')

    def gen_freqs(self, sub_news):
        tf_ctr = Counter()
        df_ctr = Counter()
        slices_lst = []
        for idx, line in tqdm(sub_news.iterrows()):
            string = line['title']
            if isinstance(line['content'], str): string += line['content']
            slices = other_utils.split_sentence_to_phrase(string)
            tf_ctr += Counter(slices)
            df_ctr += Counter(set(slices))
            slices_lst.append(slices)

        sub_news['slices'] = slices_lst
        return sub_news, tf_ctr, df_ctr
        # for idx, line in tqdm(sub_news.iterrows):
        #    tf = Counter(slices)
        #    df = Counter(set(slices))

    def slice_each_news(self):
        self.up_news, tf_up_ctr, df_up_ctr = self.gen_freqs(self.up_news)
        self.down_news, tf_down_ctr, df_down_ctr = self.gen_freqs(self.down_news)
        self.phraselst = self.gen_phrase_lst(tf_up_ctr, df_up_ctr, tf_down_ctr, df_down_ctr, len(self.up_news), len(self.down_news))
        doc_utils.phraselst_to_json(self.phraselst)
        self.up_news.to_csv(os.path.join(doc_utils.pros_pth, 'filtered_up_slices.csv'), encoding='utf_8_sig')
        self.down_news.to_csv(os.path.join(doc_utils.pros_pth, 'filtered_down_slices.csv'), encoding='utf_8_sig')


    def gen_phrase_lst(self, tf_up_ctr, df_up_ctr, tf_down_ctr, df_down_ctr, N_up, N_down):
        phraselst = []
        df_all_ctr = df_up_ctr + df_down_ctr
        for name, times in df_all_ctr.most_common():
            phraselst.append(phrase.Phrase(name=name,
                                           tf_up=tf_up_ctr[name] if name in tf_up_ctr else 0,
                                           df_up=df_up_ctr[name] if name in df_up_ctr else 0,
                                           tf_down=tf_down_ctr[name] if name in tf_down_ctr else 0,
                                           df_down=df_down_ctr[name] if name in df_down_ctr else 0,
                                           N_up=N_up,
                                           N_down=N_down))
        return phraselst



    def gen_vectors_each_news(self):
        up_pl = phraselst.Phraselst(filename='phraselist_04071712', key=lambda x: x.tf_up)
        up_pl.show_phrases()

        down_pl = phraselst.Phraselst(filename='phraselist_04071712', key=lambda x: x.tf_down)
        down_pl.show_phrases()

        up_pl_ex = up_pl - down_pl
        down_pl_ex = down_pl - up_pl
        up_pl_ex.crop(50)
        down_pl_ex.crop(50)
        up_pl_ex.show_phrases()
        down_pl_ex.show_phrases()

        all_pl_ex = up_pl_ex + down_pl_ex
        all_pl_ex.show_phrases()

        vectorizer = TfidfVectorizer(vocabulary=all_pl_ex.get_namelst(), use_idf=True)
        up_dataframe = doc_utils.csv_to_df(os.path.join(doc_utils.pros_pth, 'filtered_up_slices.csv'))
        down_dataframe = doc_utils.csv_to_df(os.path.join(doc_utils.pros_pth, 'filtered_down_slices.csv'))
        all_dataframe = pd.concat([up_dataframe, down_dataframe])
        all_dataframe['type'] = ['up' for i in range(len(up_dataframe))] + ['down' for i in range(len(down_dataframe))]
        all_slices = all_dataframe['slices']
        mx = vectorizer.fit_transform(all_slices)

        vec = []
        for i in range(mx.shape[0]):
            vec.append(mx[i])

        all_dataframe['vector'] = vec
        filepath = os.path.join(doc_utils.pros_pth,
                                'selection_{}.pkl'.format(datetime.datetime.now().strftime('%m%d%H%M')))
        all_dataframe.to_pickle(filepath)

        unsolve = pd.read_pickle(filepath)
        pass
        # df_to_csv(all_dataframe, os.path.join(pros_pth, 'selection_{}.csv'.format(datetime.datetime.now().strftime('%m%d%H%M'))))

        # from scipy import sparse
        # sparse.save_npz(os.path.join(pros_pth, 'matrix_{}.npz'.format(datetime.datetime.now().strftime('%m%d%H%M'))), mx)


def screener_test():
    sc = Screener(from_scratch=True)

if __name__ == '__main__':
    screener_test()
