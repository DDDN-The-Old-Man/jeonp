from konlpy.tag import Mecab
from konlpy.utils import pprint
from module import database as db
import json

class NLPWorker():
    nlplib = Mecab()

    @staticmethod
    def work():
        while True:
            res = db.query_db('SELECT id, body FROM article WHERE parse_b = 0 LIMIT 1000')
            print(len(res))
            if len(res) == 0:
                break

            for id_val, text in res:
                print(id_val)
                db.query_db('UPDATE article SET parse_b = 1 WHERE id = ?', [id_val])
            db.get_db().commit()
            for id_val, text in res:
                corpus = NLPWorker.nlplib.pos(text)
                sentences = NLPWorker.get_sentence(corpus)
                for sentence in sentences:
                    db.query_db('INSERT INTO parsed_article (a_id, parsed) values (?, ?)', [id_val, json.dumps(sentence)])
            db.get_db().commit()

    @staticmethod
    def get_sentence(corpus):
        result = []
        sentence = []
        for word in corpus:
            sentence.append(word)
            if not word[1] in ['EF', 'SF']:
                continue
            if len(sentence) > 1:
                result.append(list(filter(lambda x: x[-1][0] != 'S', sentence)))
                sentence = []
        return result

