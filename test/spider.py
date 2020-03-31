import re
import ast
from  urllib import parse
import time
import datetime
import  time

import requests
from scrapy import Selector
from selenium import webdriver

from models import models

main_url = 'https://bbs.csdn.net/'


#获取cookies
def get_cook():
    cookie_dict = {}
    broswer = webdriver.Chrome(executable_path=r"D:/Python/Python35/Scripts/chromedriver.exe")
    broswer.get(main_url)
    time.sleep(5)
    cook = broswer.get_cookies()
    for item in cook:
        cookie_dict[item["name"]] = item["value"]
    return cookie_dict
def get_json():
    left_menu = requests.get('https://bbs.csdn.net/dynamic_js/left_menu.js?csdn',cookies = get_cook()).text
    # match_text = re.compile('forumNodes: (.*]),').findall(left_menu)
    text_match = re.search('forumNodes: (.*])',left_menu)
    if text_match:
        text_replace = text_match.group(1).replace('null','None')
        json_match = ast.literal_eval(text_replace)

        return json_match
    return []



url_list = []
last_url = []

# 获取菜单中的所有url
def get_url(json_text):

    for item in json_text:
        if 'url' in item:
            if item['url']:
                url_list.append(item['url'])
            if 'children' in item:
                get_url(item['children'])

# 获取一级菜单url
def get_leval_list(json_text):
    leval1_url = []
    for item in json_text:
        if 'url' in item and item['url']:
            leval1_url.append(item['url'])

    return leval1_url

# 获取最终需要的url
def get_last_url():
    json_text = get_json()
    get_url(json_text)
    leval1_url = get_leval_list(json_text)
    # 删除一级菜单url
    for url in url_list:
        if url not  in leval1_url:
            last_url.append(url)
    all_urls = []
    for url in last_url:
        '''
         实用parse.urljoin()可以拼接出完整的url,也可以避免重复添加http头，
         加入获取到的url已经有了htpp头 则不会添加main_url
        '''
        # 待解决的url
        all_urls.append(parse.urljoin(main_url,url))
        # 推荐精华的url
        all_urls.append(parse.urljoin(main_url,url+'/recommend'))
        # 已解决的url
        all_urls.append(parse.urljoin(main_url,url+'/closed'))
    return all_urls

#解析话题详情页基本信息
def parse_topic_content(url,cookie):
    topic_id = re.compile('http.*?(\d+).*?').findall(url)[0]
    res_text = requests.get(url,cookies = cookie).text
    sel = Selector(text=res_text)
    txt = sel.xpath('//*[@class="mod_topic_wrap post topic"]/dl/dd/div[1]/text()').extract()

    res = ''.join(txt).strip().split('\n')
    content = ''.join(res)

    jtl = sel.xpath('.//div[@class="close_topic"]//text()').extract()[0].strip().split(' ')[1]
    praised_num = sel.xpath('.//label[@class="red_praise digg"]/em/text()').extract()[0]
    return content,jtl,praised_num

# 解析单个话题详情页
def parse_topic_page(url,cookie):
    topic_id = re.compile('http.*?(\d+).*?').findall(url)[0]
    res_text = requests.get(url,cookies = cookie).text
    sel = Selector(text=res_text)
    all_divs = sel.xpath('//div[starts-with(@id,"post-")]')
    # content_ = all_divs[0].xpath('.//div[@class="post_body post_body_min_h"]/text()').extract()[0]    #帖子的主要内容
    # print(type(content_))
    # topic_praised_num = int(all_divs[0].xpath('.//label[@class="red_praise digg"]/em/text()').extract()[0])  #获取帖子的点赞数
    # jtl_str = all_divs[0].xpath('.//div[@class="close_topic"]/text()').extract()[0]
    # jtl = 0
    # jtl_match = re.search('(\d+)%',jtl_str)
    # if jtl_match:
    #     jtl = jtl_match.group(1)
    for answer_item in all_divs[1:]:
        answer = models.Answer()
        answer.topic_id = int(topic_id)

        author_id = answer_item.xpath('.//div[@class="nick_name"]/a[1]/text()').extract()[0]
        answer.author = author_id

        create_time = datetime.datetime.strptime(answer_item.xpath('.//label[@class="date_time"]/text()').extract()[0],"%Y-%m-%d %H:%M:%S")
        answer.create_time = create_time

        content = answer_item.xpath('.//div[@class="post_body post_body_min_h"]/text()').extract()[0]
        answer.content = content

        praised_num = answer_item.xpath('.//label[@class="red_praise digg"]/em/text()').extract()[0]
        answer.parised_num = praised_num

        answer.save()

        # existed_topic = models.Topic.select().where(models.Topic.Topic_ID == topic_id)
        # if existed_topic:
        #     topic = existed_topic[0]
        #     topic.content = content_
        #     # topic.jtl = jtl
        #     # topic.praised_nums = topic_praised_num
        #     topic.save()
        # else:
        #     pass

    next_page = sel.xpath('//a[@class="pageliststy next_page"]/@href').extract()
    if next_page:
        next_url = parse.urljoin(main_url,next_page[0])
        parse_topic_page(next_url,cookie)



def parse_author_page(url,cookie):
#解析作者信息详情页
    pass


def parse_list_page(url,cookie):
# 解析topic列表详情页面

    res_html = requests.get(url,cookies = cookie).text

    sel = Selector(text = res_html)
    # 通过xpath获取表头以下的tr
    page_str = sel.xpath('.//div[@class="page_nav"]//a[last()-1]/text()').extract()
    if page_str:
        page = int(page_str[0])
    else:
        page = 1

    for i in range(0,page):
        url_ = url+'?page='+str(i+1)
        print(url_)

        res_html = requests.get(url_, cookies=cookie).text
        sel = Selector(text=res_html)
        if len(sel.xpath('//table[@class="forums_tab_table"]//tbody//tr//td/text()').extract()[0].strip()) == 0:
            all_tr = sel.xpath('.//table[@class="forums_tab_table"]//tbody//tr')  # 在xpath解析中 ·表示当前路径
            #all_tr = sel.xpath('//table[@class="forums_tab_table"]//tr')[2:]
            for tr in all_tr:
                status = tr.xpath(".//td[1]/span/text()").extract()[0]
                source = tr.xpath(".//td[2]/em/text()").extract()[0]
                topic_url = parse.urljoin(main_url,tr.xpath(".//td[3]/a[last()]/@href").extract()[0])
                print(topic_url)
                topic_id = topic_url.split('/')[-1]
                topic_title = tr.xpath(".//td[3]/a[last()]/text()").extract()[0]
                author_url = parse.urljoin(main_url,tr.xpath(".//td[4]/a/@href").extract()[0])
                author_id = author_url.split('/')[-1]
                create_time = datetime.datetime.strptime(tr.xpath(".//td[4]/em/text()").extract()[0],"%Y-%m-%d %H:%M")
                answer_info = tr.xpath(".//td[5]/span/text()").extract()[0]
                answer_num = answer_info.split('/')[0]
                click_num = answer_info.split('/')[1]
                time2 = tr.xpath(".//td[6]/em/text()").extract()[0]
                last_time = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M")
                res = parse_topic_content(topic_url,cookie)
                print(res)

                topic = models.Topic()
                topic.Topic_ID = int(topic_id)
                topic.title = topic_title
                topic.content = res[0]
                topic.author = author_id
                topic.click_num = int(click_num)
                topic.answer_num = int(answer_num)
                topic.create_time = create_time
                topic.last_answer_time = last_time
                topic.score = int(source)
                topic.status = status

                topic.jtl = res[1]
                topic.praised_nums = res[2]
                id = int(topic_id)


                # 检查是否存在topic.id
                existed_topic = models.Topic.select().where(models.Topic.Topic_ID == id)
                if existed_topic:
                    print('数据重复')
                    topic.save()
                else:
                    topic.save(force_insert=True)
                    parse_topic_content(topic_url,cookie)

        else:
            print("此页无数据")
            continue
    #     # parse_topic_page(topic_url,cook)
    #
    # next_page = sel.xpath('.//a[@class="pageliststy next_page"]/@href').extract()
    # if next_page:
     #    next_url = parse.urljoin(main_url,next_page[0])
    #     parse_list_page(next_url,cookie)
    # else:
    #     pass
# cookie = get_cook(main_url)

cook = get_cook()

urls = get_last_url()
for url in urls:
    parse_list_page(url,cook)




