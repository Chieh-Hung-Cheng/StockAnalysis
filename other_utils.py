import re

def has_digit(str):
    return bool(re.search(r'\d', str))


def split_sentence_to_phrase(sentence):
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
    return [i.strip(' -') for i in slices if len(i.strip(' -')) >= 2 and not has_digit(i.strip())]