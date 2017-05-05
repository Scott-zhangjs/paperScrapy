# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests
from paperScrapy.tools.mysqlpool import MysqlPool


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page=3):

        self.dbpool = MysqlPool
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        # self.get_proxies()

        # self.get_proxies_nt() # 透明
        self.get_proxies_nn() # 高匿
        # self.get_proxies_wn() # https
        # self.get_proxies_wt() # http

    def get_proxies_nt(self):
        page = 1#random.randint(1, 10)
        page_stop = 5#page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def get_proxies_nn(self):
        page = 1#random.randint(1, 10)
        page_stop = 20#page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def get_proxies_wt(self):
        # page = random.randint(1, 10)
        page = 1
        page_stop = 20#page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/wt/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def get_proxies_wn(self):
        # page = random.randint(1, 10)
        page = 1
        page_stop = 5#page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/wn/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print ('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print ('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0: break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            # print 'woyaokande-----', proxies
            try:
                if requests.get('https://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    print ('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                print ('fail %s' % proxy)


    # 写数据库
    def write_to_sql(self):

        ans = []
        if len(self.proxies):
            return
        for proxy in self.proxies:
            protocol = 'https' if 'https' in proxy else 'http'
            ans.append([protocol, proxy])
        insert_sql = "INSERT INTO proxies(proxies_type, proxies_link, proxies_status) VALUES (%s, %s, 1)"
        self.dbpool.insertMany(insert_sql, ans)
        self.dbpool.end()

    # 读数据库
    def read_sql(self):

        ans = []
        read_sql = "select proxie_link from proxies where proxies_status = '1'"
        ans_map = self.dbpool.getAll(read_sql)
        for map_proxy in ans_map:
            ans.append(map_proxy['proxie_link'])
        self.proxies = ans

    # 删除无效的
    def del_sql(self):

        read_sql = "select proxie_link from proxies where proxies_status = '1'"
        ans_map = self.dbpool.getAll(read_sql)
        for map_proxy in ans_map:
            tmp = map_proxy['proxie_link']
            if tmp not in self.proxies:
                del_sql = "delete from proxies where proxie_link = %s"
                self.dbpool.delete(del_sql, tmp)

        self.dbpool.end()






if __name__ == '__main__':

    # a = Proxies()
    # a.verify_proxies()
    # print (a.proxies)
    # proxie = a.proxies
    # with open('proxies.txt', 'w') as f:
    #     for proxy in proxie:
    #         f.write(proxy + '\n')

    # 生成验证写数据库
    print '------------生成-----------'
    a = Proxies()
    a.verify_proxies()
    print (a.proxies)
    a.write_to_sql()

    # 自检
    print '------------自检-----------'
    a.read_sql()
    a.verify_proxies()
    a.del_sql()


