# -*- coding:utf-8 -*-

import MySQLdb
from scrapy.utils.project import get_project_settings  # 导入seetings配置


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self):
        self.settings = get_project_settings()  # 获取settings配置，设置需要的信息

        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    # 连接到mysql，不是连接到具体的数据库
    def connectMysql(self):
        conn = MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               # db=self.db,不指定数据库名
                               charset='utf8')  # 要指定编码，否则中文可能乱码
        return conn

    # 连接到具体的数据库（settings中设置的MYSQL_DBNAME）
    def connectDatabase(self):
        conn = MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')  # 要指定编码，否则中文可能乱码
        return conn

        # 创建数据库

    def createDatabase(self):
        '''因为创建数据库直接修改settings中的配置MYSQL_DBNAME即可，所以就不要传sql语句了'''
        conn = self.connectMysql()  # 连接数据库

        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)  # 执行sql语句
        cur.close()
        conn.close()

    # 创建表
    def createTable(self, sql):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 查找数据
    def select(self, sql, *params):  # 注意这里params要加*,因为传递过来的是元组，*表示参数个数不定
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        ans = cur.fetchall()    # 获得结果中的所有数据

        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

        return ans      # 返回tuple类型数据

    # 插入数据
    def insert(self, sql, *params):  # 注意这里params要加*,因为传递过来的是元组，*表示参数个数不定
        conn = self.connectDatabase()

        cur = conn.cursor();
        cur.execute(sql, params)
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    # 更新数据
    def update(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    # 删除数据
    def delete(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


'''测试DBHelper的类'''


if __name__ == "__main__":


    dbh = DBHelper()  # 使用数据库类进行操作

    # 查询ccf中为进行dblp匹配的第一个
    sql_select = "SELECT CCF_id, CCF_name, CCF_abbreviation, CCF_type " \
                 "FROM ccf WHERE CCF_id<10000000 AND CCF_dblpname IS NULL"

    ccf_set = dbh.select(sql_select, )  # 记录所有待查询的ccf集合

    for ccf in ccf_set:
        print ccf






    # testDBHelper.testCreateDatebase()  #执行测试创建数据库
    # testDBHelper.testCreateTable()     #执行测试创建表
    # testDBHelper.testInsert()          #执行测试插入数据
    # testDBHelper.testUpdate()          #执行测试更新数据
    # testDBHelper.testDelete()          #执行测试删除数据