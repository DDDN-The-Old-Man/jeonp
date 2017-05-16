from module import database as db
import json

class ContextWorker():
    SEARCH_QUERY = 'SELECT id, body FROM article WHERE context_b = 0 AND parse_b = 1 LIMIT 100'
    PARSE_QUERY = 'SELECT id, a_id, parsed FROM parsed_article WHERE a_id = ?'
    fake_words = ['가짜']

    @staticmethod
    def work():
        while True:
            res = db.query_db(ContextWorker.SEARCH_QUERY)
            print(len(res))
            if len(res) == 0:
                break
            for id_val, _ in res:
                db.query_db('UPDATE article SET context_b = 1 WHERE id = ?', [id_val])
            db.get_db().commit()

            for id_val, _ in res:
                parsed = db.query_db(ContextWorker.PARSE_QUERY, [id_val])
                context_val = 0.0
                for p_id, a_id, js in parsed:
                    dat = json.loads(js)
                    fake_cnt = 0
                    for d in dat:
                        if d[0] in ContextWorker.fake_words:
                            fake_cnt += 1
                    if context_val < float(fake_cnt) / (len(dat) + 1):
                        context_val = float(fake_cnt) / (len(dat) + 1)

                db.query_db('INSERT INTO context (id, context_val) values (?, ?)', \
                            [id_val, context_val])
            db.get_db().commit()

