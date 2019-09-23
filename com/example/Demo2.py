import requests
from lxml import etree
import os
import re
from urllib import request
import threading
from queue import Queue

"""
    爬取最新斗图图片，网址：http://www.doutula.com/
    方式：多线程
    编写爬取代码时网页代码见resource/斗图网页.html
"""
class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            # 从page_queue队列中获取页面的url
            url = self.page_queue.get()
            self.parse_page(url)
            print("===Producer  run=======")

    def parse_page(self,url):
        response = requests.get(url,headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        images = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
        for image in images:
            # print(etree.tostring(image))
            img_url = image.get("data-original")
            alt = image.get("alt")
            alt = re.sub(r"[\?？，。！,!\*]","",alt)
            suffix = os.path.splitext(img_url)[1]
            fileName = alt + suffix
            self.img_queue.put((img_url,fileName))
            print(fileName)


class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                return
            img_url,fileName = self.img_queue.get()
            request.urlretrieve(img_url,'images/'+fileName)
            print(fileName+  "下载完成！")

def main():
    page_queue = Queue(10)
    img_queue = Queue(100) # 定义10个队列（队列数最好大一点，避免由于队列的等待导致执行时间延长）
    # 爬取1——10页的表情包
    for x in range(1,11):
        url = "http://www.doutula.com/photo/list/?page=%d" % x
        page_queue.put(url)
    # 创建5个生产者线程
    for x in range(5):
        t = Producer(page_queue,img_queue)
        t.start()
    # 创建5个消费者线程
    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()