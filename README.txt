----------------------------Created in 4.29 2017-------------------------------
1. 本项目主要任务是爬去相关论文的信息

2. mysqlpool.py 自定义了一个mysql的连接池函数，便于使用

3. spiders/dblpSpider.py 对ccf或者core给定一个venue名称，找到dblp数据库中对应的dblp名称

4. 当前任务，加入代理

当前数据情况
core中dblpname也已经更新完成。下面对数据进行一点整理：
1. venue表中共有22288个venue，其中4472个venue为"NOT IN DBLP"， 936个venue末尾带括号，最后在匹配时候应该去掉括号；
	大概20%的venue不在dblp中
2. CCF表中共有572个venue（包含一个NOT IN CCF），其中38个venue为"NOT IN DBLP"， 6%的venue不在dblp中，
   有29个venue存在第二个dblp名（但是有些和第一个是一样的）， 有8个venue存在第三个dblp名。
3. CORE表中共有2566个venue（包含一个NOT IN CORE），其中379个venue为"NOT IN DBLP"，14%的venue不在dblp中，
   有44个venue存在第二个dblp名（但是有些和第一个是一样的）， 有12个venue存在第三个dblp名。
4. CCF表中：
	A: 68个，3个NOT IN DBLP
	B: 230个，10个NOT IN DBLP
	C: 273个，25个NOT IN DBLP
5. CORE表中：
	A*: 124个，14个NOT IN DBLP
	A : 387个， 49个NOT IN DBLP
	B : 679个， 99个NOT IN DBLP
	C : 1258个， 211个NOT IN DBLP
	Australasian: 78个（均为会议）
	其他：39个

----------------------------Updated  in 5.1 2017-------------------------------
1. 代理设置完毕，速度堪忧

2. 发现新的问题，
	（1）dblp 搜索 Information Processing Letters，volume解析出现问题
	（2）Decision Support Systems，exact matches 多个链接
	（3）Foundations of Computational Mathematics，第一个volume为空
	（4）Journal of Theoretical and Applied Information Technology，Journal of Computer Information Systems，Library and Information Research，Library and Information Science Research，Libres: Library and Information Science Research Electronic Journal

3. 手动更新了core中的：
3004 Foundations of Computational Mathematics

最新数据整理：

1. CCF表中共有572个venue（包含一个NOT IN CCF），其中28个venue为"NOT IN DBLP"， 4.9%的venue不在dblp中，
   有30个venue存在第二个dblp名（但是有些和第一个是一样的）， 有8个venue存在第三个dblp名。
2. CORE表中共有2566个venue（包含一个NOT IN CORE），其中370个venue为"NOT IN DBLP"，14%的venue不在dblp中，
   有45个venue存在第二个dblp名（但是有些和第一个是一样的）， 有12个venue存在第三个dblp名。
3. CCF表中：
	A: 68个，1个NOT IN DBLP
	B: 230个，8个NOT IN DBLP
	C: 273个，18个NOT IN DBLP
4. CORE表中：
	A*: 124个，12个NOT IN DBLP
	A : 387个， 45个NOT IN DBLP
	B : 679个， 99个NOT IN DBLP
	C : 1258个， 208个NOT IN DBLP
	Australasian: 78个（均为会议）
	其他：39个


----------------------------Updated  in 5.4 2017-------------------------------
1. 发现新问题，搜索框中的特殊字符替换问题，
Computers & Security-------------Computers 

更改如下：
line = venue_name.replace("%", "%25").replace(" ", "%20").replace(",", "%2C")\
                .replace(":", "%3A").replace("?", "%3F").replace("&", "%26").replace("'", "%27")
2.启用代理，速度

3.ccf
手动更新了：
	ccf_id
	342
	262
	382
	
	core
	3004 Foundations of Computational Mathematics


3.更新数据
1. CCF表中共有572个venue（包含一个NOT IN CCF），
	312个conference
	259个journal
	其中24个venue为"NOT IN DBLP"， 4%的venue不在dblp中，
   	有29个venue存在第二个dblp名（但是有些和第一个是一样的），
	有8个venue存在第三个dblp名。
2. CORE表中共有2566个venue（包含一个NOT IN CORE），
	1702个conference
	863个journal
	其中370个venue为"NOT IN DBLP"，14.5%的venue不在dblp中，
 	有45个venue存在第二个dblp名（但是有些和第一个是一样的）， 
	有12个venue存在第三个dblp名。
3. CCF表中：
	A: 68个，0个NOT IN DBLP
	B: 230个，8个NOT IN DBLP
	C: 273个，16个NOT IN DBLP
4. CORE表中：
	A*: 124个，12个NOT IN DBLP
	A : 387个， 45个NOT IN DBLP
	B : 679个， 99个NOT IN DBLP
	C : 1258个， 208个NOT IN DBLP
	Australasian: 78个（均为会议）
	其他：39个

----------------------------Updated  in 5.16 2017-------------------------------
1. CCF和CORE表的新发现
	a. 存在3个ccf name 重复, 原因是一个venue属于不同的computercategory
	# CCF_id, CCF_name, CCF_abbreviation, CCF_dblpname, CCF_type, CCF_classification, computercategory_computerCategory_id, CCF_dblpname2, CCF_dblpname3
	'265', 'Data and Knowledge Engineering', 'DKE', 'NOT IN DBLP', 'journal', 'B', '5', NULL, NULL
	'423', 'Data and Knowledge Engineering', 'DKE', 'NOT IN DBLP', 'journal', 'B', '8', NULL, NULL
	'278', 'Information Processing Letters', 'IPL', 'Inf. Process. Lett.', 'journal', 'C', '5', NULL, NULL
	'339', 'Information Processing Letters', '', 'Inf. Process. Lett.', 'journal', 'C', '6', NULL, NULL
	'282', 'International Journal of Intelligent Systems', 'IJIS', 'Int. J. Intell. Syst.', 'journal', 'C', '5', NULL, NULL
	'459', 'International Journal of Intelligent Systems', 'IJIS', 'Int. J. Intell. Syst.', 'journal', 'C', '8', NULL, NULL

	b. 









