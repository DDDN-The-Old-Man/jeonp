from difflib import SequenceMatcher
from konlpy.tag import Mecab
from konlpy.utils import pprint
import pickle

def decode_text(text):
    decoded = False
    types = ['utf-8', 'euc-kr']
    for t in types:
        try:
            text = text.decode(t)
            decoded = True
        except:
            pass
        if decoded:
            break

    if decoded:
        return text
    return str(text)

def get_similarity(text1, text2):
    seq = SequenceMatcher(None, text1, text2)
    r = seq.ratio() / 2
    r *= len(text1) + len(text2)
    r /= len(text1)
    return r


class NLProcessor():
    def __init__(self):
        self.nlplib = Mecab()

    def load_pickle(self, pickle_path):
        corpus_list = []
        for d in dat:
            corpus_list.append(self.nlplib.pos(d))
        return corpus_list

    def get_sentence(self, corpus):
        result = []
        sentence = []
        for word in corpus:
            sentence.append(word)
            if not word[1] in ['EF', 'SF']:
                continue
            if len(sentence) > 1:
                result.append(sentence)
                sentence = []
        return result

    def make_graph(self, sentences):
        edge_h = {}
        for sen in sentences:
            for w1, w2 in zip(sen[:-1], sen[1:]):
                edge_h[(w1, w2)] = edge_h.get((w1, w2), 0) + 1

        a = list(edge_h.items())
        a = sorted(a, key=lambda x:-x[1])
        return [a, edge_h]

def find_similar(pickle_path, query):
    nlp = NLProcessor()
    c2 = nlp.nlplib.pos(query)
    pprint(c2)

    with open(pickle_path, 'rb') as f:
        texts = pickle.load(f)

    result = []

    for text in texts:
        if not text:
            continue
        c = nlp.nlplib.pos(text)
        ss = nlp.get_sentence(c)
        seq = SequenceMatcher(None, c2)
        for s in ss:
            seq.set_seq2(s)
            r = seq.ratio()
            r = r / 2
            r *= len(c2) + len(s)
            r /= len(c2)
            if r >= 0.6:
                result.append((query, s, c, int(r*100000)/1000, text))
    return result
