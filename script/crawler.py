from module.extractor import NaverExtractor
from module import strlib
import sys, pickle

arg_set = [
            ['박근혜', 'park.pickle', '%B9%DA%B1%D9%C7%FD', 1], \
            ['최순실', 'choi.pickle', '%C3%D6%BC%F8%BD%C7', 1], \
            ['세월호', 'sewol.pickle', '%BC%BC%BF%F9%C8%A3', 1], \
            #['김정은', 'kje.pickle', '%B1%E8%C1%A4%C0%BA', 1], \
            #['반기문', 'bgm.pickle', '%B9%DD%B1%E2%B9%AE', 1], \
            #['노무현', 'nmh.pickle', '%B3%EB%B9%AB%C7%F6', 1], \
            #['4월 27일', 'war.pickle', '4%BF%F9+27%C0%CF', 1], \
            #['중국군', 'cnarmy.pickle', '%C1%DF%B1%B9%B1%BA', 1]
          ]

if __name__ == "__main__":
    for argv in arg_set:
        output_file = argv[1]
        query_str = argv[2]
        to_page = argv[3]

        e = NaverExtractor()
        result = e.search_news(query_str, to_page)
        with open(output_file, 'wb') as f:
            pickle.dump(result, f)
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
