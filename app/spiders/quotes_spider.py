import scrapy
import re

douban_domain = "movie.douban.com"


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = [douban_domain]
    start_urls = ["https://movie.douban.com/subject/6860160/"]

    def parse(self, response):
        if re.match("^https://movie.douban.com/subject/[0-9]+/?$", response.url):
            self.decode_movie_page(response)

        links = response.xpath("//a")
        for link in links:
            href = link.attrib.get("href")
            if href:
                if re.match("/", href):
                    href = "https://" + douban_domain + href
                elif not re.match("https://", href):
                    # 去除非法链接
                    continue
                # 去除用户页、评论页、问答页
                elif re.match("^\S+/(people|gallery/topic|review|question|comment|photo)\S+$", href):
                    continue

                # 为了避免重复，去除url参数
                try:
                    href = href[0:href.index("?")]
                except ValueError:
                    continue

                yield scrapy.Request(href, callback=self.parse)

    @staticmethod
    def decode_movie_page(response):
        # Found a Movie
        movie_id = response.url.split("https://movie.douban.com/subject/")[1].split("/")[0]
        movie_title = response.xpath("//title/text()").get("data").replace(" ", "").replace("\n", "").split("(")[0]
        movie_url = response.url
        movie_directors = [i.root for i in response.xpath("//div[@id='info'][1]/span[1]//a/text()")]
        movie_writers = [i.root for i in response.xpath("//div[@id='info'][1]/span[2]//a/text()")]
        movie_actors = [i.root for i in response.xpath("//div[@id='info'][1]/span[3]//a/text()")]
        movie_type = [i.root for i in response.xpath("//div[@id='info'][1]/span[@property='v:genre']/text()")]
        movie_tags = [i.root for i in response.xpath("//div[@class='tags-body']/a/text()")]
        try:
            movie_rat = int(response.xpath("//strong[@class='ll rating_num'][1]/text()").get("data")
                            .replace(".", ""))
        except ValueError:
            movie_rat = 0

        print("标题：", movie_title)
        print("编号：", movie_id)
        print("网址：", movie_url)
        print("评分：", movie_rat)
        print("导演：", movie_directors)
        print("编剧：", movie_writers)
        print("主演：", movie_actors)
        print("类型：", movie_type)
        print("标签：", movie_tags, "\n\n")