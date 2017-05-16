from module import database as db
from module.nlp_parser import NLPParser
import json

class NLPWorker():
    @staticmethod
    def work():
        while True:
            res = db.query_db('SELECT id, body FROM article WHERE parse_b = 0 LIMIT 1000')
            if len(res) == 0:
                break

            for id_val, text in res:
                print(id_val)
                db.query_db('UPDATE article SET parse_b = 1 WHERE id = ?', [id_val])
            db.get_db().commit()
            for id_val, text in res:
                corpus = NLPParser.parse(text)
                sentences = NLPParser.get_sentence(corpus)
                for sentence in sentences:
                    db.query_db('INSERT INTO parsed_article (a_id, parsed) values (?, ?)', [id_val, json.dumps(sentence)])
            db.get_db().commit()

