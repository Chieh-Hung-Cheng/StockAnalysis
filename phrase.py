import math
import doc_utils
import monpa
from monpa import utils


class Phrase:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.tf_all = self.tf_up + self.tf_down
        self.df_all = self.df_up + self.df_down
        self.N_all = self.N_up + self.N_down
        for elm in ['up', 'down']:
            self.calc_MI(elm)
            self.calc_tfidf(elm)
            self.calc_assocs(elm)
            self.calc_chisq(elm)

    def calc_MI(self, lmttyp):
        # MI = log(N(XY) / (N(X)N(Y)), belongs to df
        if lmttyp == 'up':
            self.MI_up = math.log((self.df_up + 1e-4) / (self.N_up * self.df_all))
        elif lmttyp == 'down':
            self.MI_down = math.log((self.df_down + 1e-4) / (self.N_down * self.df_all))

    def calc_tfidf(self, lmttyp):
        # tf-idf = (1+log(tf)) * log(N_all/df) ???
        N_tmp = self.N_up if lmttyp == 'up' else self.N_down
        if lmttyp == 'up':
            self.tfidf_up = (1 + math.log(self.tf_up + 1e-4)) * math.log(self.N_all / self.df_all)
        elif lmttyp == 'down':
            self.tfidf_down = (1 + math.log(self.tf_down + 1e-4)) * math.log(self.N_all / self.df_all)

    def calc_assocs(self, lmttyp):
        # Support P(XY) = N(XY)/N_all
        # Confidence(X->Y) P(Y|X) = P(XY)/P(X) = N(XY)/N(X)
        # Lift P(XY)/(P(X)P(Y)) = N_all*N(XY)/(N(X)N(Y))
        # Feature (X) -> up or down (Y)
        if lmttyp == 'up':
            self.supp_up = self.df_up / self.N_all
            self.conf_up = self.df_up / self.df_all
            self.lift_up = (self.N_all * self.df_up) / (self.df_all * self.N_up)
        elif lmttyp == 'down':
            self.supp_down = self.df_down / self.N_all
            self.conf_down = self.df_down / self.df_all
            self.lift_down = (self.N_all * self.df_down) / (self.df_all * self.N_down)

    def calc_chisq(self, lmttyp):
        if lmttyp == 'up':
            expected = self.df_all * self.N_up / self.N_all
            self.chisq_up = (1 if self.df_up > expected else -1) * (self.df_up - expected) ** 2 / expected
        elif lmttyp == 'down':
            expected = self.df_all * self.N_down / self.N_all
            self.chisq_down = (1 if self.df_down > expected else -1) * (self.df_down - expected) ** 2 / expected


def split_sentence_to_phrase(sentence):
    short_sentences = utils.short_sentence(sentence)
    slices = []
    for elm in short_sentences:
        slices += monpa.cut(elm)

    return [i for i in slices if len(i) >= 2]


if __name__ == '__main__':
    split_sentence_to_phrase(
        '一開始韓國這邊居家快篩是可以在藥妝店&藥局、網路上買到，後來大爆炸後政府禁止網路&藥妝店。這些通路販售轉由便利商店&藥局販售，每人每天限購5個，每個6000韓幣，大約150台幣左右')
