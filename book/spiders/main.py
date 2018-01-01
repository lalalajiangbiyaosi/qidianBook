import scrapy
from scrapy.http import FormRequest
import time
import json
import pymysql
import re
from scrapy.loader import ItemLoader
from book.items import BiqugeItem,Book_content_Item
chanId = {
    '玄幻' : '21',
    '奇幻' : '1',
    '武侠' : '2',
    '仙侠' : '22',
    '都市' : '4',
    '现实' : '15',
    '军事' : '6',
    '历史' : '5',
    '游戏' : '7',
    '体育' : '8',
    '科幻' : '9',
    '灵异' : '10',
}

class biquge_crawler(scrapy.Spider):
    # https://www.qidian.com/all?chanId=21&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=2
    name = "biquge_crawler"    #爬虫名称
    start_urls = ['https://www.qidian.com/all?chanId=21&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1']   #启动网址
    headers = {}
    custom_settings = {
        'Host': 'www.qu.la',
        'Referer': 'http:/www.qu.la/',
        'Upgrade-Insecure-Requests': '1',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3026.3 Safari/537.36'
    }
    def parse(self,response):
        csrf = re.compile(r'(_csrf[a-zA-Z]+)=(\w+?);')
        print(response.headers.getlist('Set-Cookie'))
        for cookie_frag in [r.decode() for r in response.headers.getlist('Set-Cookie')]:
            if '_csrf' in cookie_frag:
                csrf_value = csrf.findall(cookie_frag)[0][-1]

        base_url = 'https://www.qidian.com/all?chanId={}&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page={}'
        for chanid in chanId.values():
            for page in range(1,100) :
            # for page in range(1,2) :
                url = base_url.format(chanid,page)
                yield scrapy.http.Request(url,callback=self.parse_title,meta={'_csrfToken':csrf_value})
    def parse_title(self,response):
        # print(response.body.decode('utf-8'))
        # print('--------------------')
        # print(response.meta)
        # print('--------------------')
        # item = response.meta['_csrfToken']
        base = 'https:'
        for link in response.css('div.book-img-text li h4 a::attr(href)').extract():
            url = ''.join([base,link])
            chapter_url = ''.join([url,'#Catalog'])
            # yield scrapy.http.Request(url=chapter_url,callback=self.parse_book_chapter)
            yield scrapy.http.Request(url=url,callback=self.parse_book_index,meta={'_csrfToken':response.meta['_csrfToken']})

            print(link)
    def parse_book_index(self,response):
        item = BiqugeItem()
        item['name'] = response.css('div.book-info h1 em::text')[0].extract()
        item['author'] = response.css('div.book-info h1 a::text')[0].extract()
        item['category'] = response.css('div.book-info p.tag a::text')[0].extract()
        complicated_info = response.css('div.book-info p:nth-last-child(2) em::text').extract()
        item['word_number'] = complicated_info[0]
        item['click_count'] = complicated_info[1]
        item['hot_share'] = complicated_info[2]
        item['brief'] = ''.join(response.css('div.book-intro p::text').extract())
        item['image_add'] = response.css('div.book-img img::attr(src)')[0].extract()
        # print(book_title,book_author,category,book_intro,book_number,click_count)
        yield item
        # print('--------------------------------------')
        Book_name = response.css('div.book-info h1 em::text')[0].extract()
        ajaxUrl = 'https://book.qidian.com/ajax/book/category?_csrfToken={}&bookId={}'
        bookId = response.url.split('/')[-1]
        print(bookId)
        csrf_value = response.meta['_csrfToken']
        print('--------------------')
        print(response.meta)
        print('--------------------')
        # csrf = re.compile(r'(_csrf[a-zA-Z]+)=(\w+?);')
        # print(response.headers.getlist('Set-Cookie'))
        # for cookie_frag in [r.decode() for r in response.headers.getlist('Set-Cookie')]:
        #     if '_csrf' in cookie_frag:
        #         csrf_value = csrf.findall(cookie_frag)[0][-1]
        yield scrapy.Request(url=ajaxUrl.format(csrf_value, bookId), callback=self.parse_json,meta={'book_name':Book_name})


    def parse_json(self,response):
        # print(response.body.decode())
        longJson = json.loads(response.body.decode())
        # 当存在感谢，推广介绍这类文章时，将会出现list排列
        for i in longJson['data']['vs']:
            for chap_frag in i['cs']:
                item = Book_content_Item()
                item['chapter_id'] = chap_frag['uuid']
                item['chapter_name'] = chap_frag['cN']
                item['book_name'] = response.meta['book_name']
                # item = ItemLoader(item=Book_content_Item(),response=response)
                # item.add_value('chapter_id',chap_frag['uuid'])
                # item.add_value('chapter_name',chap_frag['cN'])
                # item.add_value('book_name',response.meta['book_name'])
                # return item.load_item()
                return item
            # print(chap_frag)
    # def parse(self, response): #登录步骤
    #     formadata = {
    #         'password': '密码',
    #         'phone_num': '手机号',
    #         'email': '邮箱号二选一'
    #     }
    #     return FormRequest.from_response(
    #                               url='https://www.zhihu.com/login/{}'.format('phone_num'
    #                                                                       if formadata['phone_num'] else 'email'), # post 的网址
    #                               method="POST", # 也是默认值, 其实不需要指定
    #                               response=response,
    #                               formxpath='//form[1]', # 使用第一个form, 其实就是默认的, 这里明确写出来
    #                               formdata=formadata, # 我们填写的表单数据
    #                               callback=self.after_login, # 登录完成之后的处理
    #                               dont_click=True)
    # def after_login(self,response):

