import scrapy
import re

douban_domain = "movie.douban.com"


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = [douban_domain]
    start_urls = [
        "https://movie.douban.com/subject/26810318/",
        "https://movie.douban.com/subject/26336252/"
    ]

    def parse(self, response):
        if re.match("^https://movie.douban.com/subject/", response.url):
            # Found a Movie
            movie_id = response.url.split("https://movie.douban.com/subject/")[1].split("/")[0]
            movie_title = response.xpath("//title/text()").get("data").replace(" ", "").replace("\n", "").split("(")[0]
            movie_url = response.url

            print(movie_id, end=" ")
            print(movie_url, end=" ")
            print(movie_title)

        links = response.xpath("//a")
        for link in links:
            href = link.attrib.get("href")
            if href:
                if re.match("/", href):
                    href = "https://" + douban_domain + href
                elif not re.match("https://", href):
                    continue

                # 为了避免重复，去除url参数
                try:
                    href = href[0:href.index("?")]
                except ValueError:
                    pass

                # yield scrapy.Request(href, callback=self.parse)
