import json
import os

import requests
import re
import time
#爬虫类

class Spider:
    def __init__(self):
        self.session = requests.Session()
    def run(self, start_url):
        img_ids = self.get_img_item_ids(start_url)
        for img_id in img_ids:
            img_item = self.get_img_item_info(img_id)
            self.save_img(img_item)
    #下载器
    def download(self,url):
        try:
            return self.session.get(url)
        except Exception as e:
            print(e)
    #获取图片的id
    def get_img_item_ids(self,start_url):
        response = self.download(start_url)
        if response:
            html = response.text
            ids  = re.findall(r'http://tu.duowan.com/gallery/(\d+).html',html)
            return set(ids)
    #根据套图id获取套图的信息
    def get_img_item_info(self,img_id):
        img_item_url = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=%s&_=%s" %(img_id,int(time.time()*1000))
        response = self.download(img_item_url)
        if response:
            return json.loads(response.text)
    #根据套图的信息，持久化
    def save_img(self, img_item):
        dir_name = img_item['gallery_title']
        print(dir_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        for img_info in img_item['picInfo']:
            img_name = img_info['title']
            img_url  = img_info['url']
            pix = img_url.split('/')[-1].split('.')[-1]
            img_path = os.path.join(dir_name,"%s.%s" %(img_name,pix))
            if not os.path.exists(img_path):
                response = self.download(img_url)
                print(img_url)
                if response:
                    img_data = response.content
                    with open(img_path,'wb') as f:
                        f.write(img_data)

            print(img_path)

        # pass


if  __name__ == '__main__':
    spider = Spider()
    start_url = "http://tu.duowan.com/m/bxgif"
    spider.run(start_url)
