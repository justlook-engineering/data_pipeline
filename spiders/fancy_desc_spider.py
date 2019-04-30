import scrapy
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import pandas as pd


class FancyDescSpider(scrapy.Spider):
    name = "fancydesc"

    def start_requests(self):
        df = pd.read_excel(
            '/Users/aldrinclement/Downloads/scraper/fancy/fancy/product_catalog_v2.xlsx', sheetname='Sheet1')
        urls = df['url'].tolist()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self):
        opts = Options()
        opts.set_headless()
        assert opts.headless  # Operating in headless mode
        self.driver = Firefox(options=opts)

    def parse(self, response):
        self.driver.get(response.url)
        page = self.driver.find_element_by_xpath(
            '//body/div[@id="overlay-thing"]/div/div/div/div/div/div').get_attribute("value")
        desc = self.driver.find_element_by_xpath(
            '//body/div[@id="overlay-thing"]/div/div/div/div/div/div/div[2]/div/div')
        title = self.driver.find_element_by_xpath(
            '//body/div[@id="overlay-thing"]/div/div/aside/div/div/h3')
        estDeliveryTime = self.driver.find_element_by_xpath(
            '//body/div[@id="overlay-thing"]/div/div/aside/div/div/div/div/ul/li[1]')
        returns = self.driver.find_element_by_xpath(
            '//body/div[@id="overlay-thing"]/div/div/aside/div/div/div/div/ul/li[2]')
        imgArr = []
        images = self.driver.find_element_by_xpath(
            '//body/div[@id="overlay-thing"]/div/div/div/div/div/div/div/ul').find_elements_by_tag_name("li")
        for image in images:
            imgArr.append(image.get_attribute('innerHTML'))

        yield {
            'name': title.text,
            'desc': desc.get_attribute('innerHTML'),
            'estDeliveryTime': estDeliveryTime.get_attribute('innerHTML'),
            'returns': returns.text,
            'images': imgArr,
            'url': response.url
        }
