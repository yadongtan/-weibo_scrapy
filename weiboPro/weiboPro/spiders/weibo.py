import scrapy
from copy import deepcopy
from time import sleep
import json
from lxml import etree


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    start_urls = ['https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6']
    home_page = "https://s.weibo.com/"
    #携带cookie发起请求
    def start_requests(self):
        cookies = ""
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    #分析热搜和链接
    def parse(self, response, **kwargs):
        page_text = response.text
        with open('first.html','w',encoding='utf-8') as fp:
            fp.write(page_text)
        item = {}
        tr = response.xpath('//*[@id="pl_top_realtimehot"]/table//tr')[1:]
        #print(tr)
        for t in tr:
            item['title'] = t.xpath('./td[2]//text()').extract()[1]
            print('title : ',item['title'])
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
            detail_url = self.home_page + t.xpath('./td[2]//@href').extract_first()
            item['href'] = detail_url
            print("href:",item['href'])

            #print(item )
            #yield item
            yield scrapy.Request(detail_url,callback=self.parse_item, meta={'item':deepcopy(item)})
            # print("parse完成")
            sleep(3)
        # title = "重邮封校封出密接"
        # item['title'] = title
        # item['href'] = "https://s.weibo.com/weibo?q="+title
        # yield scrapy.Request(item['href'],callback=self.parse_item, meta={'item':deepcopy(item)})
            #print(item)
#       item{'title':href,}

    #分析每种热搜下的各种首页消息
    def parse_item(self, response, **kwargs):
        # print("开始parse_item")
        item = response.meta['item']
        #print(item)
        div_list = response.xpath('//div[@id="pl_feedlist_index"]//div[@class="card-wrap"]')[1:]
        #print('--------------')
        #print(div_list)
        #details_url_list = []
        #print("div_list : ",div_list)
        #创建名字为标题的文本存储热搜
        name = item['title']
        file_path = './' + name
        for div in div_list:
            author = div.xpath('.//div[@class="info"]/div[2]/a/@nick-name').extract_first()
            brief_con = div.xpath('.//p[@node-type="feed_list_content_full"]//text()').extract()
            if brief_con is None:
                brief_con = div.xpath('.//p[@class="txt"]//text()').extract()
            brief_con = ''.join(brief_con)
            print("brief_con : ",brief_con)
            link = div.xpath('.//p[@class="from"]/a/@href').extract_first()

            if author is None or link is None:
                continue
            link = "https:" + link + '_&type=comment'
            news_id = div.xpath('./@mid').extract_first()
            print("news_id : ",news_id)
            # print(link)
            news_time = div.xpath(".//p[@class='from']/a/text()").extract()
            news_time = ''.join(news_time)
            print("news_time:", news_time)
            print("author为:",author)
            item['author'] = author
            item['news_id'] = news_id
            item['news_time'] = news_time
            item['brief_con'] = brief_con
            item['details_url'] = link
            #json链接模板:https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4577307216321742&from=singleWeiBo
            link = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id="+ news_id + "&from=singleWeiBo"
            yield scrapy.Request(link,callback=self.parse_detail,meta={'item':deepcopy(item)})


    #分析每条消息的详情和评论
    #https://weibo.com/1649173367/JwjbPDW00?refer_flag=1001030103__&type=comment
    #json数据包
    #https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4577307216321742&from=singleWeiBo&__rnd=1606879908312
    def parse_detail(self, response, **kwargs):
        item = response.meta['item']
        all= json.loads(response.text)['data']['html']
        # #print(all)
        with open('3.html','w',encoding='utf-8') as fp:
            fp.write(all)
        tree = etree.HTML(all)
        # #因为评论前有个中文的引号,正则格外的好用
        # #comment = re.findall(r'</a>：(.*?)<',all)
        # for i in comment:
        #     for w in i:
        #         if i == "\\n":
        #             comment.pop(i)
        #             break
        # with open("12.txt","w",encoding='utf-8') as fp:
        #     for i in comment:
        #         fp.write(i)
        # print(comment)
        #95-122
        div_lists = tree.xpath('.//div[@class="list_con"]')
        final_lists = []
        #print(div_lists)

        with open('13.txt', 'a', encoding='utf-8') as fp:
            for div in div_lists:
                list = []
                username = div.xpath('./div[@class="WB_text"]/a[1]/text()')[0]
                usertime = div.xpath('.//div[@class="WB_from S_txt2"]/text()')[0]
                usercontent = div.xpath('./div[@class="WB_text"]/text()')
                str = usertime + '\n' + username
                #print(username,usertime,usercontent)
                # fp.write(usertime + '\n' + username)
                for con in usercontent[1:]:
                    str += '\n' + username + '\n' + usertime + '\n' + con + '\n'
                #
                usercontent = ''.join(usercontent)
                #print('usercontent:',usercontent)
                item['username'] = username
                item['usertime'] = usertime
                item['usercontent'] = usercontent
                list.append(username)
                list.append(usertime)
                list.append(usercontent)
                final_lists.append(list)
                #item['user'] = [username,usertime,usercontent]

            item['user'] = final_lists
            yield item
