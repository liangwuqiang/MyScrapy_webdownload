# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['test.com']
    start_urls = ['file:///C:/Users/Administrator/PycharmProjects/myscrapy/myscrapy/spiders/test/百度.html']

    def parse(self, response):
        filename = 'outputs/test.html'
        try:
            with open(filename, 'wb') as f:
                f.write(response.body)
            print('ok')
        except IOError as e:
            print(e)
        pass
