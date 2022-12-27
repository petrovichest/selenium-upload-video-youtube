import requests
from bs4 import BeautifulSoup


class GetRandomCite:

    def return_cite(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; XMP-6250 Build/HAWK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36 ADAPI/2.0 (UUID:9e7df0ed-2a5c-4a19-bec7-2cc54800f99d) RK3188-ADAPI/1.2.84.533 (MODEL:XMP-6250)', }
        sess = requests.Session()
        sess.headers.update(header)
        try:
            cite_page = sess.request('GET', 'https://quote-citation.com/random')
            soup = BeautifulSoup(cite_page.text, 'html.parser')
            cite_element = soup.findAll("div", {"class": "quote-text"})
            cite_text = cite_element[0].findAll('p')[0].text
            return cite_text
        except:
            return False

if __name__ == '__main__':
    print(GetRandomCite().return_cite())