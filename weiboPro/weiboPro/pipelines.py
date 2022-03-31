# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
class WeiboproPipeline:
    name = "weibo"
    fp = None
    def open_spider(self,spider):
        print("starting...")

    def process_item(self, item, spider):

        title = item['title']
        href = item['href']
        author = item['author']
        news_time = item['news_time']
        brief_con = item['brief_con']
        details_url = item['details_url']
        news_id = item['news_id']
        #username = item['username']
        #usertime = item['usertime']
        #usercontent = item['usercontent']
        user = item['user']
        filepath = './' + title + '.txt'
        with open(filepath,'a',encoding='utf-8') as fp:
            fp.write('title:\n' + title + '\n' + 'href:\n'+href + '\n' +'author:\n' + author + '\n' + 'news_time:\n' +news_time + '\n' + 'brief_con\n' + brief_con + '\n' +'details_url:\n' + details_url + '\n' +'news_id'+news_id + '\n')
            for u in user:
                fp.write('username:'+u[0] + '\n' + u[1] + '\n' +'usercontent:\n'+u[2] + '\n\n\n')
            fp.write('---------------------------------------------------------\n')
        fp.close()
        return item


