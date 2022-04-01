import phrase
import doc_utils


class Manipulator:
    def __init__(self):
        self.phrase_lst = doc_utils.json_2_phraselst()

    def filter(self, **kwargs):
        ret_phrase_lst = self.phrase_lst.copy()
        for key, val in kwargs.items():
            ret_phrase_lst = [i for i in ret_phrase_lst if i.__dict__[key] >= val]
        return ret_phrase_lst

    def crop(self, pl, nums=1000):
        return pl[0:nums]

    def sort_phrase_list(self, fun):
        self.phrase_lst.sort(key=fun, reverse=True)

    def show_phrase_list(self, nums=100):
        for idx, elm in enumerate(self.phrase_lst[0:nums]):
            print('{} {}'.format(idx, elm))
        if nums < len(self.phrase_lst): print('...Omitting {} elements'.format(len(self.phrase_lst) - nums))

    def show_name_list(self, nums=100):
        cnt = 0
        for elm in self.phrase_lst[0:nums]:
            print('{}'.format(elm.name), end='、')
            if cnt == 9:
                cnt = 0
                print('')
            else:
                cnt += 1
        if nums < len(self.phrase_lst): print('...Omitting {} elements'.format(len(self.phrase_lst)-nums))
        print('Num: {}\n'.format(len(self.phrase_lst)))

    def filter_crop_phrase_list(self, **kwargs):
        ret_phrase_lst = self.filter(kwargs)
        if 'nums' in kwargs: ret_phrase_lst = self.crop(ret_phrase_lst, nums=kwargs['nums'])
        return ret_phrase_lst

    def __sub__(self, other):
        ret_phrase_lst = self.phrase_lst.copy()
        return [i for i in ret_phrase_lst if i not in other]



def manipulator_test():
    manip = Manipulator()
    x = lambda i: i.tfidf_up
    manip.sort_phrase_list(x)
    manip.show_name_list()
    pass


if __name__ == '__main__':
    manipulator_test()
