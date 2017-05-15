from module.extractor import NaverExtractor
from module import strlib
from lib import database as db
import sys, pickle, hashlib

class Crawler:
    ARG_SET = [
                ['박근혜', '%B9%DA%B1%D9%C7%FD', 50000], \
                ['최순실', '%C3%D6%BC%F8%BD%C7', 50000], \
                ['세월호', '%BC%BC%BF%F9%C8%A3', 50000], \
              ]
    INSERT_QUERY = 'INSERT INTO article (u_id, title, body, url, created_at) values (?, ?, ?, ?, ?);'

    @staticmethod
    def load():
        for argv in Crawler.ARG_SET:
            query_str = argv[1]
            to_page = argv[2]

            extractor = NaverExtractor()
            url = extractor.get_start_url(query_str)

            for i in range(1, to_page):
                print("PAGE: {}".format(i))
                result = extractor.search_news(url, i)
                print("RESULT COUNT: {}".format(len(result)))
                news_result = result['news_result']
                next_url = result['next_url']
                for r in news_result:
                    u_id = hashlib.sha256(r['url'].encode('utf-8')).hexdigest()
                    try:
                        res = db.query_db(Crawler.INSERT_QUERY,
                                          [u_id, r['title'], r['body'], r['url'], r['created_at']] )
                    except Exception as e:
                        print(e)
                db.get_db().commit()
                if next_url:
                    url = next_url
                else:
                    break
'''

args2 = [['data/kje.pickle', '김정은, 전쟁 대비해 평양서 60만명 내보내'],
        ['data/bgm.pickle', '반기문, 한국 대통령 출마는 유엔법 위반'],
        ['data/bgm.pickle', '반기문, 대통령 출마 UN 출마제동 가능'],
        ['data/nmh.pickle', '노무현, 일본 소녀 성폭행'],
        ['data/war.pickle', '4월 27일 그믐에 한반도에서 전쟁'],
        ['data/cnarmy.pickle', '중국군 15만명 북중 접경지역 집결']]

idx = 1
for pp, q in args2:
    with open('data/{}.out'.format(idx), 'w') as f:
        result = strlib.find_similar(pp, q)
        for r in result:
            r2 = [str(x) for x in r]
            r2.pop(2)
            f.write("\t".join(r2) + "\n")
    idx += 1

div srch_result_area
  ul srch_lst
  li
    a href
paging
  a href

from extractor import Extractor
e = Extractor()
e.load_body('트럼프','http://news.naver.com/main/search/search.nhn?query=%C6%AE%B7%B3%C7%C1')

'''
