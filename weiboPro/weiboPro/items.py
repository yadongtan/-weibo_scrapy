# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #热搜标题
    title = scrapy.Field()
    #热搜的链接
    href = scrapy.Field()


    #发布每条相关热搜消息的作者
    author = scrapy.Field()
    #发布每条相关热搜消息的时间
    news_time = scrapy.Field()
    #发布每条相关热搜消息的内容
    brief_con = scrapy.Field()
    #发布每条相关热搜消息的详情链接
    details_url = scrapy.Field()
    #详情页ID,拿json必备
    news_id = scrapy.Field()

    #传入每条热搜消息微博详情页下的作者
    username = scrapy.Field()
    #传入每条热搜消息微博详情页下的时间
    usertime = scrapy.Field()
    #传入每条热搜消息微博详情页下的评论
    usercontent = scrapy.Field()

    #所有评论和人
    user = scrapy.Field()




