from bs4 import BeautifulSoup as bs
from cloudscraper import create_scraper
from random_user_agent.user_agent import UserAgent
import base64


class Scraper:
    def __init__(self):
        self.user_agent_list = UserAgent()
        self.headers = {
            "User-Agent": self.user_agent_list.get_random_user_agent(),
            "Referer": "https://chapmanganato.com/",
        }
        self.scraper = create_scraper(browser=self.headers)
        self.search_url = "https://manganato.com/search/story/"

    def getResults(self, keyword):
        parsed_keywords = keyword.lower().replace(" ", "_")
        url = self.search_url + parsed_keywords
        soup = self._cookSoup(url)
        results = [
            {
                "name": item.select_one("a")["title"],
                "img_url": item.select_one("a > img")["src"],
            }
            for item in soup.select("div.search-story-item")
        ]
        return results

    def getBookInfo(self, URL):
        soup = self._cookSoup(URL)
        div = soup.select_one("div.panel-story-info")
        results = {
            "name": div.select_one("div.story-info-right > h1").decode_contents(),
            "img_url": div.select_one("div.story-info-left > span > img.img-loading")[
                "src"
            ],
            "synopsis": div.select_one("div.panel-story-info-description")
            .decode_contents()
            .replace("\n<h3>Description :</h3>\n", "")
            .strip(),
            "chap_list": list(
                reversed(
                    [
                        {
                            "chap_name": chapter.select_one("a").decode_contents(),
                            "chap_url": chapter.select_one("a")["href"],
                            "chap_date": chapter.select_one(
                                "span[class='chapter-time text-nowrap']"
                            )["title"],
                        }
                        for chapter in soup.select(
                            "div.panel-story-chapter-list > ul > li"
                        )
                    ]
                )
            ),
        }
        return results

    def getImages(self, URL, convertBase64=False):
        soup = self._cookSoup(URL)
        results = [
            image["src"]
            if convertBase64 is not True
            else base64.b64encode(image["src"])
            for image in soup.select("div.container-chapter-reader > img")
        ]
        return results

    def _cookSoup(self, URL):
        html = self.scraper.get(URL).text
        return bs(html, "lxml")
