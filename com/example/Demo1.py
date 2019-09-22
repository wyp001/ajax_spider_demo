import requests
from lxml import etree
import os
import re
from urllib import request

"""
    爬取最新斗图图片，网址：http://www.doutula.com/
    方式：单线程
    编写爬取代码时网页代码见resource/斗图网页.html
"""

def parse_page(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    images = html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
    for image in images:
        # print(etree.tostring(image))
        image_url = image.get("data-original")
        alt = image.get("alt")
        alt = re.sub(r"[\?？，。！,!]","",alt)
        suffix = os.path.splitext(image_url)[1]
        fileName = alt + suffix
        # print(fileName)
        request.urlretrieve(image_url,"images/"+fileName)
        print(fileName,"已成功下载")

def main():
    for x in range(1,11):
        url = "http://www.doutula.com/photo/list/?page=%d" % x
        print("=============正在下载第%d页的图片===================" %x)
        parse_page(url)

if __name__ == '__main__':
    main()