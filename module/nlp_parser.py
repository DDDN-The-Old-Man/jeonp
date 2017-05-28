from konlpy.tag import Mecab
from konlpy.utils import pprint
import json

class NLPParser():
    nlplib = Mecab()

    @staticmethod
    def parse(text):
        corpus = NLPParser.nlplib.pos(text)
        return corpus

    @staticmethod
    def get_sentence(corpus):
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

