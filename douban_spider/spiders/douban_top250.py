import scrapy

from douban_spider.items import DoubanMovieItem

class DoubanTop250Spider(scrapy.Spider):
    name = "douban.top250"
    # allowed_domains = ["www,xxx,com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        movie_list = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movie_list:
            title = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract_first()

            p_texts = movie.xpath('.//div[@class="bd"]/p[1]//text()').extract()

            date = None
            director = None
            attrs = None

            if len(p_texts) >= 2:
                first_line = p_texts[0].strip()
                second_line = p_texts[1].strip()

                if '导演' in first_line:
                    if '主演' in first_line:
                        attrs_part = first_line.split('主演')[1].strip()
                        attrs = attrs_part
                    director_part = first_line.split('主演')[0].replace('导演:', '').strip()
                    director = director_part

                date = second_line.split('/')[0].strip()

            rating_num = movie.xpath('.//span[@class="rating_num"]/text()').extract_first()

            rating_people = None
            all_spans = movie.xpath('.//div[@class="bd"]/div/span/text()').extract()
            for span_text in all_spans:
                if span_text and '人评价' in span_text:
                    rating_people = span_text.replace('人评价', '').strip()
                    break

            rank = movie.xpath('.//div[@class="pic"]/em/text()').extract_first()

            item = DoubanMovieItem()
            item['rank'] = rank
            item["title"] = title
            item['director'] = director
            item["attrs"] = attrs
            item['date'] = date
            item['rating_num'] = rating_num
            item["rating_people"] = rating_people
            yield item

        for page_num in range(225,24,-25):
            next_url = 'https://movie.douban.com/top250' + f'?start={page_num}'
            yield scrapy.Request(next_url,callback=self.parse)
