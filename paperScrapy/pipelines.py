# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from paperScrapy.tools.mysqlpool import MysqlPool

class GooglePaperPipeline(object):
    '''
       保存到数据库中对应的class
          1、在settings.py文件中配置
          2、在自己实现的爬虫类中yield item,会自动执行
       '''

    dbpool = MysqlPool()

    # pipeline默认调用
    def process_item(self, item, spider):

        paper_id = item['paper_id']
        paper_nbCitation = item['paper_nbCitation']
        paper_citationURL = item['paper_citationURL']
        paper_rawURL = item['paper_rawURL']
        paper_isseen = item['paper_isseen']
        paper_pdfURL = item['paper_pdfURL']
        paper_scholarInfo = item['paper_scholarInfo']
        paper_rawInfo = item['paper_rawInfo']
        paper_relatedURL = item['paper_relatedURL']

        sql_update = "UPDATE paper SET paper_nbCitation = '%d'\
        					, paper_isseen= '%d', paper_citationURL = '%s', paper_pdfURL = '%s'\
        					, paper_rawURL= '%s', paper_scholarInfo = '%s', paper_rawInfo = '%s', paper_relatedURL = '%s'\
        					WHERE paper_id='%d'" \
                     % (paper_nbCitation, paper_isseen, paper_citationURL.replace('\'', '\\\'').strip(),
                        paper_pdfURL.replace('\'', '\\\'').strip(), paper_rawURL.replace('\'', '\\\'').strip(),
                        paper_scholarInfo.replace('\'', '\\\'').strip(), paper_rawInfo.replace('\'', '\\\'').strip(),
                        paper_relatedURL.replace('\'', '\\\'').strip(), paper_id)

        self.dbpool.update(sql_update)
        self.dbpool.end()
        print paper_id, ' is updated successful!'


class DblpPipeline(object):
    '''
    保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行
    '''

    dbpool = MysqlPool()
    ccf_sql_select = "SELECT count(*) " \
                     "FROM ccf WHERE CCF_id<10000000 AND CCF_dblpname = %s and CCF_type = 'conference'"
    core_sql_select = "SELECT count(*) " \
                      "FROM core WHERE CORE_id<10000000 AND CORE_dblpname = %s and CORE_type = 'conference'"

    num = dbpool.getOne(core_sql_select, ('NOT IN DBLP',))
    num = num['count(*)']
    print 'num is ', num
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
        # select_sql = "SELECT CCF_dblpname, CCF_dblpname2, CCF_dblpname3 " \
        #              "FROM ccf WHERE CCF_id = %s"
        # dblp_ans = self.dbpool.getAll(select_sql, (venue_id,))
        # dblp_ans = dblp_ans[0]
        # ccf_dblpname1 = dblp_ans["CCF_dblpname"]
        # ccf_dblpname2 = dblp_ans["CCF_dblpname2"]
        # ccf_dblpname3 = dblp_ans["CCF_dblpname3"]
        print 'save to sql:', dblp_name
        # 按顺序先更新前面的名称
        # if ccf_dblpname1 == "NOT IN DBLP":
        #     sql = "update ccf set CCF_dblpname = %s where CCF_id = %s "
        # elif ccf_dblpname2 is None:
        #     sql = "update ccf set CCF_dblpname2 = %s where CCF_id = %s "
        # else:
        #     sql = "update ccf set CCF_dblpname3 = %s where CCF_id = %s "

        sql = "update ccf set CCF_dblpname = %s where CCF_id = %s "
        self.dbpool.update(sql, (dblp_name, venue_id))

        self.dbpool.end()
        print venue_id, 'ccf is updated successful!'
        self.num -= 1
        print '---------- left ', self.num,'---------'

    def core_dblp(self, item):
        """
        存入core表的dblp名称
        :param item: 传递过来的内容
        :return: 
        """

        dblp_name = item["name"].strip()    #清楚开头结尾处的空格
        venue_id = item["venue_id"]

        # 查询当前对应venue_id对应的dblp 名称
        # select_sql = "SELECT CORE_dblpname, CORE_dblpname2, CORE_dblpname3 " \
        #              "FROM core WHERE CORE_id = %s"
        # dblp_ans = self.dbpool.getAll(select_sql, (venue_id,))
        # dblp_ans = dblp_ans[0]
        # core_dblpname1 = dblp_ans["CORE_dblpname"]
        # core_dblpname2 = dblp_ans["CORE_dblpname2"]
        # core_dblpname3 = dblp_ans["CORE_dblpname3"]
        print 'save to sql:', dblp_name
        # 按顺序先更新前面的名称
        # if core_dblpname1 == "NOT IN DBLP":
        #     sql = "update core set CORE_dblpname = %s where CORE_id = %s "
        # elif core_dblpname2 is None:
        #     sql = "update core set CORE_dblpname2 = %s where CORE_id = %s "
        # else:
        #     sql = "update core set CORE_dblpname3 = %s where CORE_id = %s "

        sql = "update core set CORE_dblpname = %s where CORE_id = %s "
        self.dbpool.update(sql, (dblp_name, venue_id))

        self.dbpool.end()
        print venue_id, ' core is updated successful!'
        self.num -= 1
        print '---------- left ', self.num, '---------'


class DblpPaperPipeline(object):
    '''
           保存到数据库中对应的class
              1、在settings.py文件中配置
              2、在自己实现的爬虫类中yield item,会自动执行
           '''

    dbpool = MysqlPool()

    # pipeline默认调用
    def process_item(self, item, spider):
        paper_id = item['paper_id']
        dblp_name = item['name']
        dblp_year = item['year']

        if dblp_year != -1:
            sql_update = "update targetpaper set targetPaper_dblp_name = %s, targetPaper_publicationYear = %s " \
                         "where targetPaper_id = %s"
            params = (dblp_name, dblp_year, paper_id)
        else:
            sql_update = "update targetpaper set targetPaper_dblp_name = %s " \
                         "where targetPaper_id = %s"
            params = (dblp_name, paper_id)

        # print 'params', params
        self.dbpool.update(sql_update, params)
        self.dbpool.end()
        print paper_id, ' is updated successful!'



