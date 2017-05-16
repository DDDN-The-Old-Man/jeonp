from module import database as db
from module.nlp_parser import NLPParser
from module.strlib import *
import json

class Finder:
    SEARCH_QUERY = 'SELECT id, body FROM article WHERE id > ? AND context_b = 1 AND parse_b = 1 ORDER BY id ASC LIMIT 100'
    PARSE_QUERY = 'SELECT id, a_id, parsed FROM parsed_article WHERE a_id = ?'
    CONTEXT_QUERY = 'SELECT context_val FROM context WHERE id = ?'

    @staticmethod
    def search(text):
        q = NLPParser.parse(text)
        start_id = -1

        max_sim = -1;
        max_a_id = None;
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
                if max_sim < sim:
                    max_sim = sim
                    max_a_id = a_id
        if not max_a_id:
            return 'NOT FOUND'

        res = db.query_db(Finder.CONTEXT_QUERY, [max_a_id])
        ctx_val = res[-1][0]

        adat = db.query_db('SELECT id, title, body, url FROM article WHERE id = ?', [max_a_id])
        res = { 'sim_val': max_sim, 'context_val': ctx_val }
        res['id'], res['title'], res['body'], res['url'] = adat[-1]
        return res
