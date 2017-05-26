from module import database as db
from module.nlp_parser import NLPParser
from module.strlib import *
import json
from time import time
from random import random
from multiprocessing import Process, Queue

class Finder:
    SEARCH_QUERY = 'SELECT id, body FROM article WHERE id > ? AND context_b = 1 AND parse_b = 1 ORDER BY id ASC LIMIT 10000'
    PARSE_QUERY = 'SELECT id, a_id, parsed FROM parsed_article WHERE a_id in ({})'
    CONTEXT_QUERY = 'SELECT context_val FROM context WHERE id = ?'
    SIM_DEADLINE = 0.6

    @staticmethod
    def match(sentences, q, start, interval, result):
        i = start
        t = []
        while i < len(sentences):
            o_id, a_id, js = sentences[i]
            i += interval
            dat = json.loads(js)
            dat = list(map(lambda x: tuple(x), dat))
            sim = get_similarity(q, dat)
            if sim > Finder.SIM_DEADLINE:
               t.append([sim, a_id])
        result.put(t)

    @staticmethod
    def search(text):
        st = time()
        q = NLPParser.parse(text)
        start_id = -1
        tt = time()-st; print(tt); st=time()

        result = []
        while len(result) < 10:
            res = db.query_db(Finder.SEARCH_QUERY, [start_id])
            if len(res) == 0:
                break
            ids = list(map(lambda x: x[0], res))
            if start_id < max(ids):
                start_id = max(ids)
            ids = list(map(lambda x: str(x), ids))
            ids_str = ",".join(ids)

            sentences = db.query_db(Finder.PARSE_QUERY.format(ids_str))
            p = []
            process_num = 8
            current_result = Queue()
            for i in range(process_num):
                kwargs = { 'q': q, \
                        'sentences': sentences, \
                        'start': i, \
                        'interval': process_num, \
                        'result': current_result }
                p.append( Process(target=Finder.match, kwargs=kwargs) )
            for i in range(process_num):
                p[i].start()
            for i in range(process_num):
                result += current_result.get()
            print('---------')
            print(len(result))

        result2 = []
        for sim, a_id in result:
            '''
            res = db.query_db(Finder.CONTEXT_QUERY, [a_id])
            ctx_val = res[-1][0]
            '''
            ctx_val = 0.1 * random()
            adat = db.query_db('SELECT id, title, body, url FROM article WHERE id = ?', [a_id])
            res = { 'sim_val': sim, 'context_val': ctx_val }
            res['id'], res['title'], res['body'], res['url'] = adat[-1]
            result2.append(res)
        return json.dumps(result2, indent=4, separators=(',', ': '))
