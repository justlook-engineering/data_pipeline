import scrapy


class FancySpider(scrapy.Spider):
    name = "fancyfeed"

    def start_requests(self):
        urls = [
            'https://fancy.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.xpath("//body/div/div/div/div[2]/ol/li")
        for item in items:
            img_orig_url = item.xpath(
                ".//div/figure/span/span/button/@item_img_url").get()

            if item.xpath(".//div/figure/div/video/source/@src").get():
                yield {
                    'name':  item.xpath(".//div/figcaption/a/b/text()").get(),
                    'url': 'https://fancy.com' + item.xpath(".//div/figure/a/@href").get(),
                    'regular_price':  item.xpath(".//div/figcaption/span/button/small/text()").get(),
                    'sale_price': item.xpath(".//div/figcaption/span/button/b/text()").get(),
                    'img_url': 'https://' + img_orig_url[2:],
                    'likes': item.xpath(".//div/figure/span/span/button/text()").get(),
                    'video_url': item.xpath(".//div/figure/div/video/source/@src").get(),
                    'has_video': '1',
                }
            elif item.xpath(".//div/figure/a/@href").get() is not None:
                yield {
                    'name':  item.xpath(".//div/figcaption/a/b/text()").get(),
                    'url': 'https://fancy.com' + item.xpath(".//div/figure/a/@href").get(),
                    'regular_price':  item.xpath(".//div/figcaption/span/button/small/text()").get(),
                    'sale_price': item.xpath(".//div/figcaption/span/button/b/text()").get(),
                    'img_url': 'https://' + img_orig_url[2:],
                    'likes': item.xpath(".//div/figure/span/span/button/text()").get(),
                }

        next_page = response.xpath('//body/div/div/div/div[2]/div[@class="pagination"]/a[1]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

            # print(item)

        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
