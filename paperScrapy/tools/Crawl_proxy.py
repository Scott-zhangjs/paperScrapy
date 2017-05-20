# *-* coding:utf-8 *-*
import requests
import threading

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

        self.dbpool = MysqlPool()
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
        # self.get_proxies_nn() # 高匿
        # self.get_proxies_wn() # https
        # self.get_proxies_wt() # http

    # -------------xici代理------------
    # 透明
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

    # 高匿
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

    # http
    def get_proxies_wt(self):
        # page = random.randint(1, 10)
        print'爬取--xicidaili---http--中'
        page = 1
        page_stop = 11  # page + self.page

        while page < page_stop:
            url = 'http://www.xicidaili.com/wt/%d/' % page
            try:

                html = requests.get(url, headers=self.headers).content
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.find(id='ip_list')
                for odd in ip_list.find_all(class_='odd'):
                    protocol = odd.find_all('td')[5].get_text().lower() + '://'
                    self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            except:
                print '---------解析存在问题--------------'
            print '---------完成页码----------', page
            page += 1

    # https
    def get_proxies_wn(self):
        # page = random.randint(1, 10)
        print'爬取--xicidaili---https--中'
        page = 1
        page_stop = 11#page + self.page

        while page < page_stop:
            url = 'http://www.xicidaili.com/wn/%d/' % page
            try:

                html = requests.get(url, headers=self.headers).content
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.find(id='ip_list')
                for odd in ip_list.find_all(class_='odd'):
                    protocol = odd.find_all('td')[5].get_text().lower() + '://'
                    self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            except:
                print '---------解析存在问题--------------'
            print '---------完成页码----------', page
            page += 1

    # ---------------快代理------------------
    def get_proxies_kuaidaili(self):
        # page = random.randint(1, 10)
        print'爬取--快代理--中'
        page = 1
        page_stop = 11#page + self.page
        while page < page_stop:
            url = 'http://www.kuaidaili.com/proxylist/%d/' % page # 普通代理
            # url = 'http://www.kuaidaili.com/free/outha/%d/' % page   # 国外代理
            try:

                html = requests.get(url, headers=self.headers).content
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.find(id='index_free_list') # proxylist
                # ip_list = soup.find(id='list') # 国外代理
                # print ip_list
                tr = ip_list.find_all('tr')
                # print tr
                for i in range(1, len(tr)):
                    ip_tmp = tr[i].find_all('td')[0].get_text().strip()

                    port_tmp = tr[i].find_all('td')[1].get_text().strip()
                    pro_list = tr[i].find_all('td')[3].get_text()
                    pro_list = pro_list.split(',')
                    for pro_tmp in pro_list:
                        pro_tmp = pro_tmp.strip().lower() + '://'
                        # self.proxies.append(pro_tmp + ip_tmp + ':' + port_tmp)
                        self.proxies.append('https://' + ip_tmp + ':' + port_tmp)
                        # print 'lianjie----------->', pro_tmp + ip_tmp + ':' + port_tmp
            except Exception, e:
                print e.args[0]
                print '---------解析存在问题--------------'
            print '---------完成页码----------', page
            page += 1

    # ---------------proxy360------------------

    def get_proxies_proxy360(self):
        # page = random.randint(1, 10)
        print'爬取--proxy360--中'
        page = 1
        page_stop = 2  # page + self.page
        while page < page_stop:
            url = 'http://www.proxy360.cn/default.aspx'
            try:

                html = requests.get(url, headers=self.headers).content
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.find(id='ctl00_ContentPlaceHolder1_upProjectList')
                tr = ip_list.find_all('div', class_='proxylistitem')
                for i in range(1, len(tr)):
                    ip_tmp = tr[i].find_all('span')[0].get_text().strip()
                    port_tmp = tr[i].find_all('span')[1].get_text().strip()
                    pro_list = ['http', 'https']
                    for pro_tmp in pro_list:
                        pro_tmp = pro_tmp.strip().lower() + '://'
                        self.proxies.append(pro_tmp + ip_tmp + ':' + port_tmp)
                        # print 'lianjie----------->', pro_tmp + ip_tmp + ':' + port_tmp
            except:
                print '---------解析存在问题--------------'
            print '---------完成页码----------', page
            page += 1

    # ---------------------------------------------
    # goubanjia 代理
    def get_proxies_goubanjia(self):
        # page = random.randint(1, 10)
        print'爬取--全网代理ip--中'
        page = 1
        page_stop = 21#page + self.page
        while page < page_stop:
            url = 'http://www.goubanjia.com/free/index%d.shtml' % page
            try:
                html = requests.get(url, headers=self.headers).content
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.find(class_='table')
                tr = ip_list.find_all('tr')
                # print 'tr', tr[0]
                for i in range(1, len(tr)):
                    ip_tmp = tr[i].find_all('td')[0]
                    ip_right = []
                    for tag in ip_tmp:

                        if tag.name != 'p':

                            if tag != ':':
                                ip_right.append(str(tag.text))
                            else:
                                ip_right.append(':')
                    ip_right = "".join(ip_right)
                    # print 'ip_right:', ip_right
                    pro_list = tr[i].find_all('td')[2].get_text()
                    pro_list = pro_list.split(',')
                    for pro_tmp in pro_list:
                        pro_tmp = pro_tmp.strip().lower() + '://'
                        self.proxies.append(pro_tmp + ip_right )
                        # print 'lianjie----------->', pro_tmp + ip_right
            except Exception, e:
                print e.args[0]
                print '---------解析存在问题--------------'
            print '---------完成页码----------', page
            page += 1

    # ---------------------------------------------
    # xundaili 代理
    def get_proxies_xdaili(self):
        # page = random.randint(1, 10)
        print'爬取--讯代理--中'
        page = 1
        page_stop = 2  # page + self.page
        while page < page_stop:
            url = 'http://www.xdaili.cn/freeproxy.html'
            try:
                html = requests.get(url, headers=self.headers).content
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.find(id='table1')
                tr = ip_list.find_all('tr')
                # print 'tr', tr[0]
                for i in range(1, len(tr)):
                    ip_tmp = tr[i].find_all('td')[0].get_text().strip()
                    port_tmp = tr[i].find_all('td')[1].get_text().strip()
                    pro_list = tr[i].find_all('td')[3].get_text()
                    pro_list = pro_list.split('/')
                    for pro_tmp in pro_list:

                        pro_tmp = pro_tmp.strip().lower() + '://'
                        self.proxies.append(pro_tmp + ip_tmp + ':' + port_tmp)
                            # print 'lianjie----------->', pro_tmp + ip_tmp
            except:
                print '---------解析存在问题--------------'
            print '---------完成页码----------', page
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
                if protocol == 'http':
                    # pass
                    if requests.get('http://www.qq.com/', proxies=proxies, timeout=2).status_code == 200:
                    # print 'status code is ', tmp
                    # if tmp == 200:
                        print ('success %s' % proxy)
                        new_queue.put(proxy)
                elif protocol == 'https':
                    pass
                    # if requests.get('https://scholar.google.com.hk', proxies=proxies, timeout=3).status_code == 200:
                    #     # print ('success %s' % proxy)
                    #     new_queue.put(proxy)
            except Exception, e:
                # pass
                # print e.args[0]
                print ('fail %s' % proxy)

    # 写数据库
    def write_to_sql(self):
        print '写入----数据库----中'

        ans = []
        if len(self.proxies) == 0:
            print '--------无有效代理ip-----------'
            return
        # 获取当前数据库内容
        read_sql = "select proxies_link from proxies"
        ans_map = self.dbpool.getAll(read_sql)
        ans_list = []
        if ans_map:
            ans_list = [ans_m['proxies_link'] for ans_m in ans_map]
        for proxy in self.proxies:
            # 查重
            if proxy not in ans_list:
                protocol = 'https' if 'https' in proxy else 'http'
                ans.append([protocol, proxy])
        insert_sql = "INSERT INTO proxies(proxies_type, proxies_link, proxies_status) VALUES (%s, %s, 1)"
        self.dbpool.insertMany(insert_sql, ans)
        self.dbpool.end()
        print '写入----数据库----成功'

    # 读数据库
    def read_sql(self):
        print '读取----数据库----中'

        self.proxies = []
        read_sql = "select proxies_link from proxies"
        ans_map = self.dbpool.getAll(read_sql)
        if not ans_map:
            print'数据库为空,休息一会'
            return
        for map_proxy in ans_map:
            self.proxies.append(map_proxy['proxies_link'])

    # 删除无效的
    def del_sql(self):
        print '删除----无效ip----中'
        read_sql = "select proxies_link from proxies"
        ans_map = self.dbpool.getAll(read_sql)
        for map_proxy in ans_map:
            tmp = map_proxy['proxies_link']
            if tmp not in self.proxies:
                # print '待删除-------->',tmp
                del_sql = "delete from proxies where proxies_link = %s"
                self.dbpool.delete(del_sql, (tmp,))
        self.dbpool.end()
        print '删除无效ip个数:', len(ans_map) - len(self.proxies)

    # 生成并存入数据库
    def get_insert(self):
        # 生成验证写数据库
        print '------------生成-----------'
        # self.get_proxies_nn()  # 高匿
        self.proxies = []
        self.get_proxies_proxy360()
        self.get_proxies_xdaili()
        # self.get_proxies_wt()           # xicidali--http
        self.get_proxies_kuaidaili()
        self.get_proxies_goubanjia()

        print '获取未检测ip个数:', len(self.proxies)

        # 已解决出现不对格式的ip
        # for i in range(len(self.proxies)):
        #     self.proxies[i] = str(self.proxies[i]).replace('..', '.')

        self.verify_proxies()
        print '获取有效ip个数:', len(self.proxies)
        self.write_to_sql()
        print '------------插入完毕-----------'

    def self_check(self):
        # 自检
        print '------------自检-----------'
        self.read_sql()
        if len(self.proxies) == 0:
            print '!!!!!!!!!!!数据库空!!!!!!!!!'
            time.sleep(100)     # 数据
            return
        self.verify_proxies()
        self.del_sql()
        print '------------自检完成-----------'

    def get_random_proxy_http(self):
        '''随机从数据库中读取proxy'''

        select_sql = "select proxies_link from proxies where proxies_status = 1 and proxies_type = 'http'"
        results = self.dbpool.getAll(select_sql)
        while len(results) == 0:
            print '!!!!!!!!!!!数据库空!!!!!!!!!'
            self.get_insert()
            results = self.dbpool.getAll(select_sql)
        # print '---------the results is---------', results
        res = random.choice(results)
        return res['proxies_link']

    def get_random_proxy_https(self):
        '''随机从数据库中读取proxy'''

        select_sql = "select proxies_link from proxies where proxies_status = 1 and proxies_type = 'https'"
        results = self.dbpool.getAll(select_sql)
        while not results:
            print '!!!!!!!!!!!数据库空!!!!!!!!!'
            self.get_insert()
            results = self.dbpool.getAll(select_sql)
        res = random.choice(results)
        return res['proxies_link']

    # 每五分钟插入一次
    def thread_insert(self):
        while True:
            self.get_insert()
            time.sleep(40+random.uniform(1,5))

    # 每分钟检查一次
    def thread_check(self):
        while True:
            self.self_check()
            time.sleep(100+random.uniform(1,5))


if __name__ == '__main__':

    # a = Proxies()
    # a.verify_proxies()
    # print (a.proxies)
    # proxie = a.proxies
    # with open('proxies.txt', 'w') as f:
    #     for proxy in proxie:
    #         f.write(proxy + '\n')



    a = Proxies()
    # a.get_proxies_kuaidaili()


    raw_input_do = raw_input("选择操作:\n1.插入\n2.自检\n")
    if raw_input_do == '1':
        a.thread_insert()
    else:
        a.thread_check()








