# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from paperScrapy.tools.mysqlpool import MysqlPool


class DblpPipeline(object):
    '''
    保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行
    '''

    dbpool = MysqlPool()

    # pipeline默认调用
    def process_item(self, item, spider):
        venue_type = item["venue_type"]

        if venue_type == 'CCF':
            self.ccf_dblp(item)
        elif venue_type == 'CORE':
            self.core_dblp(item)
        else:
            print 'No this type:', venue_type


    def ccf_dblp(self, item):
        """
        存入ccf的表dblp名称
        :param item: 传递过来的内容
        :return: 
        """

        dblp_name = item["name"]
        venue_id = item["venue_id"]

        # 查询当前对应venue_id对应的dblp 名称
        select_sql = "SELECT CCF_dblpname, CCF_dblpname2, CCF_dblpname3 " \
                     "FROM ccf WHERE CCF_id = %s"
        dblp_ans = self.dbpool.getAll(select_sql, (venue_id,))
        dblp_ans = dblp_ans[0]
        ccf_dblpname1 = dblp_ans["CCF_dblpname"]
        ccf_dblpname2 = dblp_ans["CCF_dblpname2"]
        ccf_dblpname3 = dblp_ans["CCF_dblpname3"]
        print 'save to sql:', dblp_name
        # 按顺序先更新前面的名称
        if ccf_dblpname1 == "NOT IN DBLP":
            sql = "update ccf set CCF_dblpname = %s where CCF_id = %s "
        elif ccf_dblpname2 is None:
            sql = "update ccf set CCF_dblpname2 = %s where CCF_id = %s "
        else:
            sql = "update ccf set CCF_dblpname3 = %s where CCF_id = %s "

        self.dbpool.update(sql, (dblp_name, venue_id))

        self.dbpool.end()
        print venue_id, 'ccf is updated successful!'

    def core_dblp(self, item):
        """
        存入core表的dblp名称
        :param item: 传递过来的内容
        :return: 
        """

        dblp_name = item["name"]
        venue_id = item["venue_id"]

        # 查询当前对应venue_id对应的dblp 名称
        select_sql = "SELECT CORE_dblpname, CORE_dblpname2, CORE_dblpname3 " \
                     "FROM core WHERE CORE_id = %s"
        dblp_ans = self.dbpool.getAll(select_sql, (venue_id,))
        dblp_ans = dblp_ans[0]
        core_dblpname1 = dblp_ans["CORE_dblpname"]
        core_dblpname2 = dblp_ans["CORE_dblpname2"]
        core_dblpname3 = dblp_ans["CORE_dblpname3"]
        print 'save to sql:', dblp_name
        # 按顺序先更新前面的名称
        if core_dblpname1 == "NOT IN DBLP":
            sql = "update core set CORE_dblpname = %s where CORE_id = %s "
        elif core_dblpname2 is None:
            sql = "update core set CORE_dblpname2 = %s where CORE_id = %s "
        else:
            sql = "update core set CORE_dblpname3 = %s where CORE_id = %s "

        self.dbpool.update(sql, (dblp_name, venue_id))

        self.dbpool.end()
        print venue_id, ' core is updated successful!'



