from module import database as db
from module.nlp_parser import NLPParser
from module.strlib import *
import json
from time import time
from random import random
from multiprocessing import Process, Queue
import hashlib

class Finder:
    SEARCH_QUERY = 'SELECT id, body FROM article WHERE id > ? AND context_b = 1 AND parse_b = 1 ORDER BY id ASC LIMIT 10000'
    PARSE_QUERY = 'SELECT id, a_id, parsed FROM parsed_article WHERE a_id in ({})'
    CONTEXT_QUERY = 'SELECT context_val FROM context WHERE id = ?'
    CACHE_QUERY = 'SELECT result FROM cached_result WHERE hash_id = ?'
    CACHE_INSERT_QUERY = 'INSERT INTO cached_result (hash_id, result) values (?, ?);'
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
        q = NLPParser.parse(text)
        start_id = -1

        hash_id = hashlib.sha256(str(q).encode('utf-8')).hexdigest()
        result = db.query_db(Finder.CACHE_QUERY, [hash_id])
        if len(result) > 0:
            result2 = [json.loads(x[0]) for x in result]
            return json.dumps(result2, indent=4, separators=(',', ': '))

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
            adat = db.query_db('SELECT id, title, body, url, created_at FROM article WHERE id = ?', [a_id])
            res = { 'sim_val': sim, 'context_val': ctx_val }
            res['id'], res['title'], res['body'], res['url'], res['c'= adat[-1]
            result2.append(res)
            db.query_db(Finder.CACHE_INSERT_QUERY, [hash_id, json.dumps(res)])
            db.get_db().commit()
        return json.dumps(result2, indent=4, separators=(',', ': '))
