# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapyChsItem
import copy
from urllib import parse
import hashlib


class ScrapyChsSpider(scrapy.Spider):
    name = 'scrapy-chs'
    allowed_domains = []
    start_urls = ['https://scrapy-chs.readthedocs.io/zh_CN/0.24/index.html']
    # start_urls = ['file:///C:/Users/Administrator/PycharmProjects/myscrapy/outputs/test.html']  # 测试

    def parse(self, response):
        try:
            item = ScrapyChsItem()
            xpath_url = '//div[@class="wy-side-scroll"]//a[@class="reference internal"]//@href'
            xpath_title = '//div[@class="wy-side-scroll"]//a[@class="reference internal"]//text()'
            urls = response.xpath(xpath_url).extract()
            titles = response.xpath(xpath_title).extract()
            for i in range(len(urls)):
                item['sn'] = i + 1
                item['title'] = titles[i]
                url = 'https://scrapy-chs.readthedocs.io/zh_CN/0.24/{url}'.format(url=urls[i])
                item['url'] = url
                yield scrapy.Request(url=url, meta={'item': copy.deepcopy(item)}, callback=self.parse_html)
                # 采用深拷贝，避免item重复，参见https://www.cnblogs.com/crawer-1/p/8017533.html
        except Exception as e:
            print('parse出错', e)
        pass

    def parse_html(self, response):
        try:
            item = response.meta['item']
            # 获取正文内容
            xpath_content = '//div[@class="section"]'
            content = response.xpath(xpath_content).extract_first()
            # 获取图片url
            item['image_urls'] = []
            xpath_image = '//*[@id="id2"]/a/img/@src'  # 图片的提取特征
            image_urls = response.xpath(xpath_image).extract()

            for image_url in image_urls:
                # 重构图片url，以供下载
                web_url = 'https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/architecture.html'  # url前缀
                full_image_url = parse.urljoin(web_url, image_url)
                item['image_urls'].append(full_image_url)
                # 用哈希码替换正文中图片的url，因为默认下载的图片文件名是哈希码
                filename = 'images/' + self.sha1(full_image_url) + '.jpg'
                content = content.replace(image_url, filename)
            item['content'] = content
            yield item
        except Exception as e:
            print('parse_html出错', e)
        pass

    @staticmethod
    def sha1(name):
        """ 将图片url转成哈希码 """
        if not isinstance(name, str):
            name = str(name)
        sha1 = hashlib.sha1()
        sha1.update(name.encode('utf-8'))
        return sha1.hexdigest()
