# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from .items import ScrapyChsItem
from scrapy.pipelines.images import ImagesPipeline
import string


class MyscrapyPipeline(object):
    @staticmethod
    def process_item(item, spider):
        try:
            if spider.name == 'scrapy-chs' and isinstance(item, ScrapyChsItem):
                # print('=== 进入管道工作 ===')
                remove = string.punctuation
                table = str.maketrans('', '', remove)
                title = item['title'].translate(table)
                filename = 'outputs/' + str(item['sn']) + '_' + title + '.html'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(item['content'])
                print(item['title'] + '......已完成')
        except Exception as e:
            print('process_item出错', e)
        return item


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        path = super(MyImagesPipeline, self).file_path(request, response, info)
        image_name = path.replace("full/", "")  # 去掉默认的full目录
        return image_name

    def get_media_requests(self, item, info):
        try:
            for image_url in item['image_urls']:
                print('图片下载>> ', image_url)
                yield scrapy.Request(image_url)
        except Exception as e:
            print('get_media_requests出错', e)
    pass
