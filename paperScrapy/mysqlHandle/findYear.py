# -*- coding: utf-8 -*-

import re
import MySQLdb


def updateSql():

    conn = MySQLdb.connect(host = '192.168.1.198',
                           port = 3306,
                           user = 'jingshuai',
                           passwd = '123456',
                           db = 'citation_raw_qian',
                           charset = 'utf8')  # 要指定编码，否则中文可能乱码

    cur = conn.cursor()
    sql_select = "select targetPaper_id as id, targetPaper_scholarInfo as info " \
                 "from targetpaper where targetpaper_publicationYear = -1"

    print 'start searching...'
    cur.execute(sql_select)
    ans = cur.fetchall()    # 获得结果中的所有数据

    print ans[0]
    print ans[0][0], ans[0][1]
    print len(ans)


    print 'start updating'
    sql_update = "update targetpaper set targetpaper_publicationYear = %s where targetPaper_id = %s"

    i = 0
    while i < len(ans)/100:
        tmp = []
        for ans1 in ans[i*100:i*100+100]:
            year = findYearRe(ans1[1])
            tmp.append((year, ans1[0]))
        # print tmp
        cur.executemany(sql_update, tmp)
        conn.commit()
        print len(ans)/100-i, 'is updated success'
        i = i+1

    for ans1 in ans[i*100:]:
        year = findYearRe(ans1[1])
        tmp.append((year, ans1[0]))
    cur.executemany(sql_update, tmp)
    conn.commit()
    print len(ans)/100-i, 'is updated success'

# 从字符串中寻找年份-----严格
def findYear(str):

    patern = r'\d*20[0|1]\d+'

    tmp = re.findall(patern, str)
    # print tmp
    i = 0
    while i < len(tmp):
        if len(tmp[i]) > 4:
            print tmp[i], 'is too long'
            tmp.pop(i)
        else:
            i = i+1

    if len(tmp) == 0:
        print 'Find no years in one info.'
        return 0        # 若无年份置0
    elif len(tmp)>1:
        myset = set(tmp)
        if len(myset) >1:
            print 'Find different years in one info.'
            return -1
        else:
            return int(tmp[0])
    else:
        return int(tmp[0])

# 从字符串中搜索年份--不严格，针对重复情况
def findYearRe(str):

    patern = r', 20[0|1]\d+'

    tmp = re.findall(patern, str)
    # print tmp
    i = 0
    while i < len(tmp):
        tmp[i] = tmp[i].replace(', ', '')
        if len(tmp[i]) > 4:
            print tmp[i], 'is too long'
            tmp.pop(i)
        else:
            i = i + 1

    if len(tmp) == 0:
        print 'Find no years in one info.'
        return 0  # 若无年份置0
    elif len(tmp) > 1:
        myset = set(tmp)
        if len(myset) > 1:
            print 'Find different years in one info.'
            return -1
        else:
            return int(tmp[0])
    else:
        return int(tmp[0])


if __name__ == '__main__':
    # str = "S Kedad-Sidhoum, F Monna, G Mounié… - Euro-Par 2013: Parallel  …, 2014 - Springer"
    # print findYearRe(str)

    updateSql()