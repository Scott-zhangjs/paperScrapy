# -*- coding: utf-8 -*-

import MySQLdb

conn = MySQLdb.connect(host = '192.168.1.198',
                       port = 3306,
                       user = 'jingshuai',
                       passwd = '123456',
                       db = 'citation_raw_qian',
                       charset = 'utf8')  # 要指定编码，否则中文可能乱码

cur = conn.cursor()
sql_select = "select paper_venue_name as vname, venue_id as id from paper, venue where venue_venue_id is null and paper_venue_name = venue_name"

print 'start searching...'
cur.execute(sql_select)
ans = cur.fetchall()    # 获得结果中的所有数据

# print ans[0]
# print ans[0][0], ans[0][1]
# print len(ans)

print 'start updating'
sql_update = "update paper set venue_venue_id = %s where paper_venue_name = %s"
i = 0
while i < len(ans)/100:
    tmp = []
    for ans1 in ans[i*100:i*100+100]:
        tmp.append((ans1[1],ans1[0]))
    # print tmp
    cur.executemany(sql_update, tmp)
    conn.commit()
    print len(ans)/100-i, 'is updated success'
    i = i+1

for ans1 in ans[i*100:]:
    tmp.append((ans1[1],ans1[0]))
cur.executemany(sql_update, tmp)
conn.commit()
print len(ans)/100-i, 'is updated success'