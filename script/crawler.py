from module.extractor import NaverExtractor
from module import strlib
from module import database as db
import sys, pickle, hashlib

class Crawler:
    ARG_SET = [
                ['박근혜', '%B9%DA%B1%D9%C7%FD', 500], \
                ['최순실', '%C3%D6%BC%F8%BD%C7', 500], \
                ['세월호', '%BC%BC%BF%F9%C8%A3', 500], \
                ['문재인', '%BC%BC%BF%F9%C8%A3', 500], \
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
