from konlpy.tag import Mecab
from konlpy.utils import pprint

class NLPParserr():
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

