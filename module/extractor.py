from bs4 import BeautifulSoup
from bs4 import NavigableString
from module import strlib
from datetime import datetime
import urllib.request
import urllib.parse
import time, random


class Extractor:
    def load_html(self, url):
        url = url.strip()
        if not url:
            return None
        try:
            time.sleep(random.random()*1+0.5) # i am not a bot
            req = urllib.request.Request(url)
        except Exception as e:
            return None
        with urllib.request.urlopen(req) as f:
            html_text = ""
            while True:
                try:
                    t = f.read()
                except http.client.IncompleteRead as icread:
                    html_text += strlib.decode_text(icread.partial)
                    continue
                else:
                    html_text += strlib.decode_text(t)
                    break
        return html_text

    def load_body(self, url, desc):
        html_text = self.load_html(url)
        soup = BeautifulSoup(html_text, 'html5lib')
        best_val = 0
        best_body = None

        created_at = soup.find('div', class_='sponsor').find('span', class_='t11').string
        for elem in soup.find_all('div', id='articleBodyContents'):
            text_set = []
            for x in elem.children:
                if isinstance(x, NavigableString):
                    text_set.append(x.strip())
            text = ' '.join(text_set)
            sim_val = strlib.get_similarity(desc, text)
            if sim_val > best_val:
                best_body = text
                best_val = sim_val
        return [created_at, best_body]


class NaverExtractor(Extractor):
    NAVER_SEARCH_URL = 'http://news.naver.com/main/search/search.nhn?query='

    def get_start_url(self, query):
        return NaverExtractor.NAVER_SEARCH_URL + query

    def search_news(self, full_url, page_id):
        news_result = []
        html_text = self.load_html(full_url)
        soup = BeautifulSoup(html_text, 'html5lib')
        for elem in soup.find('div', class_='srch_result_area') \
                        .find_all('div', class_='ct'):
            try:
                url = elem.find('div', class_='info') \
                          .find('a', class_='go_naver') \
                          .get('href')
                desc = elem.find('p', class_='dsc')
                created_at, body = self.load_body(url, ' '.join(desc.strings).strip())
                title = elem.find('div', class_='info') \
                            .find('div', class_='head_social share_area') \
                            .find('a').get('data-title')
                if url and title and body:
                    news_result.append({
                            'created_at': created_at,
                            'title': title,
                            'body': body,
                            'url': url,
                        })
            except Exception as e:
                pass

        next_url = None
        for elem in soup.find('div', class_='paging').children:
            try:
                href = elem.get('href')
                if not href:
                    continue
                href = 'http://news.naver.com' + href
                parsed_url = urllib.parse.urlparse(href)
                page_num = int(urllib.parse.parse_qs(parsed_url.query)['page'][0])
                if page_num == current_page + 1:
                    next_url = href
            except Exception as e:
                pass
        return {
            'news_result': news_result,
            'next_url': next_url
            }
