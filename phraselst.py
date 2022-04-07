import phrase
import doc_utils
import copy
import other_utils

class Phraselst:
    def __init__(self, filename='phraselist', key=None, nums=1000, **kwargs):
        self.phraselst = doc_utils.json_to_phraselst('{}.json'.format(filename))
        self.key = key
        self.filter(**kwargs)
        self.sort_phraselst(self.key)
        # self.namelst = [i.name for i in self.phraselst]
        self.crop(nums)

    def filter(self, **kwargs):
        for key, val in kwargs.items():
            self.phraselst = [i for i in self.phraselst if i.__dict__[key] >= val]
        return self.phraselst

    def crop(self, nums=1000):
        self.phraselst = self.phraselst[0:nums]

    def sort_phraselst(self, fun):
        self.phraselst.sort(key=fun, reverse=True)

    def get_namelst(self):
        return [i.name for i in self.phraselst]

    def show_phrases(self, nums=100, compact=True):
        cnt = 0
        for idx, elm in enumerate(self.phraselst[0:nums]):
            if compact:
                print('{}'.format(elm.name), end='、')
                if cnt == 9:
                    cnt = 0
                    print('')
                else:
                    cnt += 1
            else:
                print('{} {}'.format(idx, elm))
        if nums < len(self.phraselst): print('...Omitting {} elements'.format(len(self.phraselst) - nums))
        print('Total {} elements'.format(len(self.phraselst)))

    def __sub__(self, other):  # exclde
        ret_phraselst = copy.copy(self)
        ret_phraselst.phraselst = [i for i in ret_phraselst.phraselst if
                                   i.name not in [j.name for j in other.phraselst]]  # other.namelst
        return ret_phraselst

    def __add__(self, other):
        ret_phraselst = copy.copy(self)
        ret_phraselst.phraselst = self.phraselst + other.phraselst
        return ret_phraselst





def phraselst_test():
    up_pl = Phraselst(key=lambda x: x.supp_up,
                      lift_up=1.2,
                      supp_up=0,
                      conf_up=0.05
                      )
    up_pl.eliminate_digit()
    up_pl.show_phrases(compact=True)

    down_pl = Phraselst(key=lambda x: x.supp_down,
                        lift_down=1.2,
                        supp_down=0,
                        conf_down=0.05
                        )
    down_pl.show_phrases()

    up_pl_ex = up_pl.exclude(down_pl)
    down_pl_ex = down_pl.exclude(up_pl)
    up_pl_ex.show_phrases()
    down_pl_ex.show_phrases()


if __name__ == '__main__':
    phraselst_test()
