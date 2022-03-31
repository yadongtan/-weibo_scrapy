
import random
# 自定义微博请求的中间件
class WeiboproDownloaderMiddleware(object):

    def process_request(self, request, spider):
        # "设置cookie"
        cookies = "SINAGLOBAL=7445638262810.062.1606393968309; ALF=1637930004; wvr=6; SUB=_2A25yu9Q2DeRhGeBK6lsU8C7EzT-IHXVuR_x-rDV8PUJbkNANLVakkW1NR_ZQG1khNkgy2jTOs1Q367JzGK4beyDf; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWA10Xwzs6kWwQ193xmnlOu5NHD95QcSh24SK571hq0Ws4DqcjRi--fiK.XiK.7i--Xi-ihi-8si--RiK.4iKy8i--NiKnEi-z4i--RiKLWiKyWi--4i-2ciK.4IP-t; UOR=,,www.baidu.com; wb_view_log_6419500863=1536*8641.25; _s_tentry=www.baidu.com; Apache=1002481459153.9855.1606833584581; ULV=1606833584640:4:3:3:1002481459153.9855.1606833584581:1606833437232; webim_unReadCount=%7B%22time%22%3A1606834521053%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A62%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A92%2C%22msgbox%22%3A0%7D"
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        request.cookies = cookies
        #  设置ua
        ua = random.choice(spider.settings.get("USER_AGENT_LIST"))
        request.headers["User-Agent"] = ua
        return None
