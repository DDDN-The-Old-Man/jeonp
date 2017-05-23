from module import database as db
from module.nlp_parser import NLPParser
from module.strlib import *
import json

class Finder:
    SEARCH_QUERY = 'SELECT id, body FROM article WHERE id > ? AND context_b = 1 AND parse_b = 1 ORDER BY id ASC LIMIT 100'
    PARSE_QUERY = 'SELECT id, a_id, parsed FROM parsed_article WHERE a_id = ?'
    CONTEXT_QUERY = 'SELECT context_val FROM context WHERE id = ?'
    SIM_DEADLINE = 0.5

    @staticmethod
    def search(text):
        q = NLPParser.parse(text)
        start_id = -1

        result = []
        while True:
            res = db.query_db(Finder.SEARCH_QUERY, [start_id])
            if len(res) == 0:
                break
            sentences = []
            for a_id, _ in res:
                if start_id < a_id:
                    start_id = a_id
                sentences += db.query_db(Finder.PARSE_QUERY, [a_id])

            for o_id, a_id, js in sentences:
                dat = json.loads(js)
                dat = list(map(lambda x: tuple(x), dat))
                sim = get_similarity(q, dat)
                if sim > Finder.SIM_DEADLINE:
                    result.append([sim, a_id])

        result2 = []
        for sim, a_id in result:
            res = db.query_db(Finder.CONTEXT_QUERY, [a_id])
            ctx_val = res[-1][0]
            adat = db.query_db('SELECT id, title, body, url FROM article WHERE id = ?', [a_id])
            res = { 'sim_val': sim, 'context_val': ctx_val }
            res['id'], res['title'], res['body'], res['url'] = adat[-1]
            result2.append(res)

        return result2
